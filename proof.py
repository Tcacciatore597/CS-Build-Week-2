import hashlib
import requests
import sys
import json



def proof_of_work(block):
    
    """
    Simple Proof of Work Algorithm
    Stringify the block and look for a proof.
    Loop through possibilities, checking each one against `valid_proof`
    in an effort to find a number that is a valid proof
    :return: A valid proof for the provided block
    """
    block_string = json.dumps(block, sort_keys=True)
    proof = 0
    while valid_proof(block_string, proof) is False:
        proof += 1

    return proof

def valid_proof(block_string, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
    leading zeroes?  Return true if the proof is valid
    :param block_string: <string> The stringified block to use to
    check in combination with `proof`
    :param proof: <int?> The value that when combined with the
    stringified previous block results in a hash that has the
    correct number of leading zeroes.
    :return: True if the resulting hash is a valid proof, False otherwise
    """
    guess = f'{block_string}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:6] == "000000"

if __name__ == '__main__':

    coins_mined = 0

    # Run forever until interrupted
    while True:
        r = requests.get("https://lambda-treasure-hunt.herokuapp.com/api/bc/last_proof/", headers = {"Authorization": "Token b383749c19f1a7d08b8270d4f85bc5e05a47b119"})
       
        # Handle non-json response
        try:
            data = r.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            break

        new_proof = proof_of_work(data.get('proof'))

        post_data = {"proof": new_proof}

        r = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/bc/mine/", json=post_data, headers = {"Authorization": "Token b383749c19f1a7d08b8270d4f85bc5e05a47b119", "Content-Type": "application/json"})
        print(r)
        data = r.json()

        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))