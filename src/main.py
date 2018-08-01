# 5 users who want to reach concensus
# add previous hash to the other user's previous hash
# 3 leading zero's must be obtained
# create hashes with changing random nonce
# shortest search must be reacalculated by other user

import random
import string

import hashlib

import simplejson as json

def generate_nonce(length):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

nonces_array = []
nonces_users = []
all_hashes_array = []
all_hashes_users = []
block1 = []
block2 = []

def first_block():
  block = {
    'previous_hash': '0123456789abcdef',
    'timestamp': '1533095806',
    'data_from_Alice': {
      'could_be': 'anything'
    },
    'data_from_Bob': {
      'could_be': 'anything'
    },
    'data_from_Caroline': {
      'could_be': 'anything'
    },
    'data_from_Daniel': {
      'could_be': 'anything'
    },
    'data_from_Elizabeth': {
      'could_be': 'anything'
    }
  }

  global block1
  block1 = json.dumps(block)

  return block1

def create_hash():
  global nonces_array, block2

  if len(nonces_array) == 0:
    nonce = generate_nonce(5)

    block2 = [
      first_block(),
      nonce
    ]

    nonces_array.append(nonce)
    json_block = json.dumps(block2)
    hash_object = hashlib.sha256(json_block.encode())
  else:
    nonce = generate_nonce(5)

    block2.append(nonce)
    nonces_array.append(nonce)
    json_block = json.dumps(block2)
    hash_object = hashlib.sha256(json_block.encode())

  return hash_object.hexdigest()

def mine(user):
  while True:
    correct_hash = create_hash()

    global all_hashes_array
    all_hashes_array.append(correct_hash)

    if len(correct_hash) - len(correct_hash.lstrip('0')) == 1:
      global nonces_array, nonces_users, all_hashes_users
      nonces_users.append({ user: nonces_array })
      nonces_array = []

      all_hashes_users.append({ user: all_hashes_array })
      all_hashes_array = []
      
      return False

def mine_all_users():
  mine('Alice')
  mine('Bob')
  mine('Caroline')
  mine('Daniel')
  mine('Elizabeth')

def compare_lengths():
  mine_all_users()

  global nonces_users

  lowest = [ None, 10000 ]

  for i in nonces_users:
    for k, v in i.items():
      if len(v) < lowest[1]:
        lowest = [ k, len(v) ]
      elif len(v) == lowest[1]:
        lowest.append( k )

  if len(lowest) > 2:
    compare_lengths()

  recalculate_hashes(lowest[0])

def recalculate_hashes(winner):
  global nonces_users, block1, all_hashes_users

  for nu in nonces_users:
    for k1, v1 in nu.items():
      if k1 == winner:
        for hu in all_hashes_users:
          for k2, v2 in hu.items():
            if k2 == winner:
              part1 = [ block1 ]
              counter = 0
              for i in range(len(v1)):
                part1.append(v1[i])
                json_part1 = json.dumps(part1)
                hash_object = hashlib.sha256(json_part1.encode())
                hash_object_digest = hash_object.hexdigest()

                if hash_object_digest == v2[i]:
                  counter = counter + 1
                  if counter == len(v1):
                    print('A hash was found and the hash is approved by the peers')
                  elif counter < len(v1):
                    pass
                  else:
                    print('No appropriate hash found')

compare_lengths()