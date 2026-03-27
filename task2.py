import random
import matplotlib.pyplot as plt

# XOR of bits = parity (mod 2 sum of bits)
def parity(x):
    return bin(x).count("1") % 2

# same as task1's generate_LAT 
def generate_LAT(S):
    LAT = [[0]*16 for _ in range(16)]  # 16x16 LAT table
    for a in range(16):
        for b in range(16):
            count = 0
            for x in range(16):
                if parity(a & x) == parity(b & S[x]):
                    count += 1
            LAT[a][b] = count - 8  # Store bias
    return LAT

# extract the most useful linear approximations from the LAT
def get_top_lat_entries(LAT, k=15):
    entries = []

    for a in range(1, 16):   # skip trivial (a=0 or b=0) approximations
        for b in range(1, 16):
            bias = LAT[a][b]
            entries.append((a, b, bias))

    # sort by absolute bias descending
    entries.sort(key=lambda x: abs(x[2]), reverse=True)

    return entries[:k]

# key recovery using different linear approximation (with highest bias)
def key_recovery(S, a, b):

    # compute inverse S-box for decryption
    S_inv = [0]*16
    for i, v in enumerate(S):
        S_inv[v] = i

    # generate key
    K = random.randint(0,15)
    N = 10000

    # generate plaintext-ciphertext pairs
    pairs = []
    for _ in range(N):
        x = random.randint(0,15)
        y = S[x ^ K]
        pairs.append((x,y))

    # key recovery
    scores = [0]*16

    for k_guess in range(16):
        count = 0
    
        for x,y in pairs:
            # partial decryption
            v = S_inv[y] ^ k_guess
            
            if parity(a & x) == parity(b & v):
                count += 1
    
        scores[k_guess] = abs(count - len(pairs)/2) / len(pairs)  # Bias from 0.5
        #print(f"Key guess {k_guess}: count={count}, bias={scores[k_guess]:.4f}")

    # result
    recovered = scores.index(max(scores))

    #print("Real key:", K)
    #print("Recovered key:", recovered)
    #print("Scores:", scores)

    return K, recovered, max(scores)

def run_experiment(S):

    LAT = generate_LAT(S)

    top_entries = get_top_lat_entries(LAT, k=10)

    print("\nTop 10 LAT entries (a, b, bias):")
    for a, b, bias in top_entries:
        print(f"a={a:04b}, b={b:04b}, bias={bias}")

    print("\n--- Running Key Recovery ---\n")

    results = []

    for i, (a, b, bias) in enumerate(top_entries):

        print(f"\nTest {i+1}: a={a:04b}, b={b:04b}, LAT bias={bias}")

        K, recovered, score = key_recovery(S, a, b)

        success = (K == recovered)

        print(f"Real key     : {K}")
        print(f"Recovered key: {recovered}")
        print(f"Bias score   : {score:.4f}")
        print(f"Success      : {success}")

        results.append((a, b, bias, success, score))

    return results


if __name__ == "__main__":
    S = [0xE,4,0xD,1,2,0xF,0xB,8,3,0xA,6,0xC,5,9,0,7]

    run_experiment(S)
