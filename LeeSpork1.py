"""
by LeeSpork
2022-11-15

Program for "shipping" two Discord users.

version 1B.0.1
"""

"""File slightly altered for language options 2024-10-05"""

# When each bit is compared, either there will be two 0s, a 0 and a 1, or two 1s.
# Tweak these to adjust how these are weighted when computing compatability.
# Adjust values until you are happy with the Min, Max, and Mean computed from the sample data.
# Note that WEIGHT_01 is the only one that reduces the compatability, basically.
WEIGHT_00 = 1 # maybe don't touch
WEIGHT_01 = 10
WEIGHT_11 = 44

# Threshold for the bot to combine their two names when using the `ship` function.
SHIP_THRESHOLD = 0.75 # love?!
SHIP_NO_THRESHOLD =  0.25 # oh nao!!

# Which bits of the Snowflake are used/ignored when computing "compatability" of user's Discord IDs?
COMPATABILITY_BIT_MASK = ( # https://discord.com/developers/docs/reference
  "000000000000000000000000000000000001111111" # timestamp (ms since first second of 2015)
+ "11111" # Internal worker ID
+ "11111" # Internal process ID
+ "111111111111" # Increment
)

# Sample data. Please obtain more to test better.
SAMPLE_IDS = [
    (292383690313695232, "LeeSpork"),
]


def snowflake_compatability(discord_id_1:int, discord_id_2:int) -> float:
    """Returns a value from 0 to 1 using a formula to calculate the "compatability" of two Discord user's snowflake IDs.
    
    
    """
    
    # These are str that start with 0b
    bin1 = bin(discord_id_1)
    bin2 = bin(discord_id_2)
    
    # Find how many common bits there are, out of the bits in the bit mask
    total = 0
    compatable = 0
    
    # Reverse iterate thru characters in BIT_MASK str
    for i in range(-1, -len(COMPATABILITY_BIT_MASK)-1, -1):
        
        # Mask
        if COMPATABILITY_BIT_MASK[i] == '0': continue
        
        # If out of range, all subsequent characters will be 0.
        if bin1[i] == 'b': bin1 = "0"*64
        if bin2[i] == 'b': bin2 = "0"*64
        
        # There are 3 cases:
        #   0 and 0,
        #   0 and 1 or 1 and 0,
        # & 1 and 1.
        if (bin1[i] == bin2[i]):
            if bin1[i] == '1':
                # Case 1 and 1
                compatable += WEIGHT_11
                total += WEIGHT_11
            else:
                # assume Case 0 and 0
                compatable += WEIGHT_00
                total += WEIGHT_00
        else:
            # assume Case 0 and 1 or 1 and 0,
            # compatable += 0
            total += WEIGHT_01
    
    return compatable / total


def snowflake_compatability_percentage(discord_id_1:int, discord_id_2:int) -> str:
    """Returns a string from 0% to 100% using a formula to calculate the "compatability" of two Discord user's snowflake IDs."""
    return f"{snowflake_compatability(discord_id_1, discord_id_2):.0%}"


def ship_names(name_dom:str, name_sub:str) -> str:
    """Combines the two names."""
    return name_dom[:len(name_dom)//2] + name_sub[len(name_sub)//2:]


def ship(name1:str, discord_id_1:int, name2:str, discord_id_2:int, english:bool=False) -> str:
    compatability = snowflake_compatability(discord_id_1, discord_id_2)
    string = ["O nível de amor é ","Estimated love level is "][english] + f"{compatability:.0%}."
    if (compatability > SHIP_THRESHOLD):
        string += f" \"{ship_names(name1, name2)}\"?!"
    elif (compatability < SHIP_NO_THRESHOLD):
        string += [" Oh não..."," Oh no..."][english]
    return string



def debug_snowflake(snowflake:int):
    b = bin(snowflake + 0b10000000000000000000000000000000000000000000000000000000000000000)[3:]
    return f"{b[:42]} {b[42:42+5]} {b[42+5:42+5+5]} {b[42+5+5:42+5+5+12]}"


def debug_mask():
    b = COMPATABILITY_BIT_MASK.replace('0', '.')
    return f"{b[:42]} {b[42:42+5]} {b[42+5:42+5+5]} {b[42+5+5:42+5+5+12]}"


def debug_print_binarys():
    print("Sample Discord user ID Snowflakes:")
    print(f"{debug_mask()} (mask)")
    
    for i in SAMPLE_IDS:
        print(f"{debug_snowflake(i[0])} {i[1]}")

def debug_all_compatabilities(samples=SAMPLE_IDS, show_all_values=True, alert_100=True, show_progress=True, out:list=None):
    print(f"Computing compatabilities of all possible pairings of {len(samples)} sample users\n(Except with themselves)...")
    
    values = []
    maximum = 0.0
    minimum = 1.0
    names = []
    
    num_100_percent = 0
    num_above_threshold = 0
    num_bellow_threshold = 0
    
    n = len(samples)
    
    if (show_progress):
        estimated_pairings_n = n**2//2-n//2
        ccount = 0
        ccent = None
    
    # COMPUTE!! O(n^2)
    for i in range(n):
        
        for j in range(i+1, n): # only do half of the pairings since it is symmetrical
            
            if (show_progress):
                ccount += 1
                cccent = f"{ccount/estimated_pairings_n:.0%}"
                if ccent != cccent:
                    print(cccent)
                ccent = cccent
            
            a = samples[i]
            b = samples[j]
            
            v = snowflake_compatability(a[0], b[0])
            
            values.append(v)
            
            if v >= maximum:
                maximum = v
                
            if v <= minimum:
                minimum = v
                
            names.append(f"{a[1]} and {b[1]}")
            
            if (v > SHIP_THRESHOLD):
                num_above_threshold += 1
                
                if (v == 1):
                    num_100_percent += 1
                    if (alert_100):
                        print(f"<@{a[0]}> and <@{b[0]}> have a compatability of 100%.")
            
            elif (v < SHIP_NO_THRESHOLD):
                num_bellow_threshold += 1
    
    # Display stats
    print(f"Completed computing {len(values)} pairings.")
    print(f"Min : {minimum}")
    print(f"Max : {maximum}")
    print(f"Mean: {sum(values)/len(values)}")
    print(f"{num_bellow_threshold} ({num_bellow_threshold/len(values):.3%}) pairings are under the Oh No! threshold.")
    print(f"{num_above_threshold} ({num_above_threshold/len(values):.3%}) pairings are over the love threshold.")
    print(f"{num_100_percent} ({num_100_percent/len(values):.3%}) pairings have 100% compatability.")
    
    # Display the result of every matching, in order.
    if (show_all_values):
        print(f"\nAll values:")    
        newl = [i for i in range(len(values))]
        def key(w): return values[w]
        newl.sort(key=key)
        last = None
        for i in newl:
            if values[i] == last:
                print(f"  \"   - {names[i]}")
            else:
                print(f"{values[i]:.1%} - {names[i]}")
            last = values[i]
    
    # Add results to output
    if (out is not None):
        for i in values:
            out.append(i)
    
    

if __name__ == "__main__":
    line = "--------"
    print(line)
    debug_print_binarys()
    print(line)
    debug_all_compatabilities()
    print(line)
