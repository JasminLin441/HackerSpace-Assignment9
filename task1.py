import random

# XOR of bits = parity (mod 2 sum of bits)
def parity(x):
    return bin(x).count('1') % 2  # Count number of 1s and take mod 2 for parity


def generate_LAT(S):
    LAT = [[0]*16 for _ in range(16)]  # 16x16 LAT table
    for a in range(16): # iterate over mask a
        for b in range(16): # iterate over mask b
            count = 0
            for x in range(16): # iterate over all possible inputs
                if parity(a & x) == parity(b & S[x]): # check if linear approximation holds
                    count += 1
            LAT[a][b] = count - 8  # Store bias
    return LAT

# extract the most useful linear approximations from the LAT (for task 2)
def extract_approximations(LAT): 
    approximations = []
    for a in range(1,16):
        for b in range(1,16):
            bias = LAT[a][b] / 16 # Normalize bias to range [-0.5, 0.5]
            if abs(bias) > 0:   # keep useful ones
                approximations.append((a, b, bias))
    
    approximations.sort(key=lambda x: abs(x[2]), reverse=True)  # Sort by absolute bias
    for a,b,bias in approximations[:5]:
        print(f"a={a:04b}, b={b:04b}, bias={bias}")

    return approximations[:5]  # Return top 5 approximations


if __name__ == "__main__":
    S = [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8, 0x3, 0xA, 0x6, 0xC, 0x5,0x9,0x0,0x7]
    LAT= generate_LAT(S)
    for row in LAT:
        print(row)
    approximations=extract_approximations(LAT)
