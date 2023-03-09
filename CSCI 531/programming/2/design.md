# CSCI 531 Programming Assignment 2 Design Document

The purpose of this project is to write three Python 3 scripts (`buildmtree.py`, `checkinclusion.py`, and `checkconsistency.py`) that implement three Merkle tree operations: building a Merkle tree, checking whether a data item is in an existing Merkle tree, and checking whether the new version of a Merkle tree is consistent with the old one. The main design goals of this project are correctness and understandability of implementation. That's why we use recursion to implement these operations, mostly following their recursive definition in RFC 6962, rather than opt for a potentially faster iterative implementation. The code length for each operation is around only 10 lines of code.

The only persistent data are the Merkle trees serialized in JSON files. The serialization format for a Merkle tree is described with the JSON schema below:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Merkle Tree",
  "description": "A Merkle tree",
  "type": "object",
  "properties": {
    "hash": {
      "type": "string",
      "description": "The SHA-256 hash of the Merkle tree node."
    },
    "size": {
      "type": "integer",
      "description": "The size of the subtree rooted at this node.",
      "minimum": 0
    },
    "left": {
      "$ref": "#"
    },
    "right": {
      "$ref": "#"
    }
  },
  "required": ["hash", "size"]
}
```

The only dependency for our implementation is a Python 3 interpreter with its standard library. The scripts provide command-line interfaces with help messages available by passing the `-h` argument.

## Implementation

1. `buildmtree.py`
    1. Building a Merkle tree is implemented with the function `build(data: Sequence[bytes]) -> dict[str]` which returns the constructed Merkle tree as a `dict`. `buildmtree.py` then saves the Merkle tree to the file "merkle.tree" according to the serialization format described above.
    2. We adopt RFC 6962's algorithm for handling odd number of items: If there are an odd number of nodes at a level, the last node won't be duplicated but is directly moved up one level instead. Here is an example of a constructed Merkle tree for 3 items from Section 2.1.3. of RFC 6962:
        ```
            hash0
            / \
           /   \
          /     \
          g      c
         / \     |
         a b     d2
         | |
        d0 d1
        ```
    3. The command-line argument format for `buildmtree.py` is slightly tweaked for easier parsing. Here is an example:
        ```
        python3 buildmtree.py alice bob carlol david
        ```
2. `checkinclusion.py`: The tree is read from the file merkle.tree and then deserialized. Checking whether an item is included in a tree is implemented by `include(digest: str, tree: dict[str]) -> Optional[list[str]]`.
3. `checkconsistency.py`
    1. The command-line argument format is again adjusted. The script takes two arguments and both must be a JSON string that represents arrays of data items. The first argument is the old list and the second argument is the new one. Here is an example:
        ```
        > python3 checkconsistency.py '["alice", "bob", "carlol", "david"]' '["alice", "bob", "carlol", "david", "eve", "fred"]'
        ```
    2. Two Merkle trees are constructed from the lists and saved to the file "merkle.trees" in JSON. The format is `{"old": <old-tree>, "new": <new-tree>}` with the individual trees conforming to the schema above.
    3. Then, the consistency of two trees is checked by the function `consistent(old_tree: dict[str], new_tree: dict[str]) -> Optional[list[str]]`, whose return value is a proof of consistency represented list of hex digests. The first element of the proof is the old tree root's hash and the last element is new tree root's hash. If the two trees are exactly the same, then it only contains one hash. Elements in between are intermediate nodes' hash values that prove the consistency between the two trees. The proof itself is serialized as a JSON array and printed to the standard output.

## Demo

Due to the length of the demo, the texts for the terminal session is reproduced below instead of a screenshot.

```
> python3 buildmtree.py alice bob carlol david
> cat merkle.tree
{
    "hash": "b1833ecfe5a6c8aeae767ac902d2188cd3efd63bc3f9b45a0eb98a6812029198",
    "size": 4,
    "left": {
        "hash": "cb57721dc3aa8df0eef91989560b053a86be98131f45650bd1c3955e0167ef17",
        "size": 2,
        "left": {
            "hash": "2bd806c97f0e00af1a1fc3328fa763a9269723c8db8fac4f93af71db186d6e90",
            "size": 1
        },
        "right": {
            "hash": "81b637d8fcd2c6da6359e6963113a1170de795e4b725b84d1e0b4cfd9ec58ce9",
            "size": 1
        }
    },
    "right": {
        "hash": "e5e27c7f259cb9a773b66fb3675ba1bae0ac36d1c9e9dc59eaaab7a1a0a21c56",
        "size": 2,
        "left": {
            "hash": "5d9896af338ff832d279efd9fac6694c77118a8a5c42425dac1827ea41f97e2a",
            "size": 1
        },
        "right": {
            "hash": "07d046d5fac12b3f82daf5035b9aae86db5adc8275ebfbf05ec83005a4a8ba3e",
            "size": 1
        }
    }
}
> python3 checkinclusion.py richard
No
> python3 checkinclusion.py david
Yes ["5d9896af338ff832d279efd9fac6694c77118a8a5c42425dac1827ea41f97e2a", "cb57721dc3aa8df0eef91989560b053a86be98131f45650bd1c3955e0167ef17"]
> python3 checkconsistency.py '["alice", "bob", "carlol", "david"]' '["alice", "bob", "carlol", "david", "eve", "fred"]'
Yes ["b1833ecfe5a6c8aeae767ac902d2188cd3efd63bc3f9b45a0eb98a6812029198", "c3800c31c1335f0c8c3d2b5a461077561ee4693c72407436064708238f5a29ad", "7d373b4db976b2ae43804bdaac8b171a049ea4dd87a6e858ecf121eb9c4ba51b"]
> cat merkle.trees
{
    "old": {
        "hash": "b1833ecfe5a6c8aeae767ac902d2188cd3efd63bc3f9b45a0eb98a6812029198",
        "size": 4,
        "left": {
            "hash": "cb57721dc3aa8df0eef91989560b053a86be98131f45650bd1c3955e0167ef17",
            "size": 2,
            "left": {
                "hash": "2bd806c97f0e00af1a1fc3328fa763a9269723c8db8fac4f93af71db186d6e90",
                "size": 1
            },
            "right": {
                "hash": "81b637d8fcd2c6da6359e6963113a1170de795e4b725b84d1e0b4cfd9ec58ce9",
                "size": 1
            }
        },
        "right": {
            "hash": "e5e27c7f259cb9a773b66fb3675ba1bae0ac36d1c9e9dc59eaaab7a1a0a21c56",
            "size": 2,
            "left": {
                "hash": "5d9896af338ff832d279efd9fac6694c77118a8a5c42425dac1827ea41f97e2a",
                "size": 1
            },
            "right": {
                "hash": "07d046d5fac12b3f82daf5035b9aae86db5adc8275ebfbf05ec83005a4a8ba3e",
                "size": 1
            }
        }
    },
    "new": {
        "hash": "7d373b4db976b2ae43804bdaac8b171a049ea4dd87a6e858ecf121eb9c4ba51b",
        "size": 6,
        "left": {
            "hash": "b1833ecfe5a6c8aeae767ac902d2188cd3efd63bc3f9b45a0eb98a6812029198",
            "size": 4,
            "left": {
                "hash": "cb57721dc3aa8df0eef91989560b053a86be98131f45650bd1c3955e0167ef17",
                "size": 2,
                "left": {
                    "hash": "2bd806c97f0e00af1a1fc3328fa763a9269723c8db8fac4f93af71db186d6e90",
                    "size": 1
                },
                "right": {
                    "hash": "81b637d8fcd2c6da6359e6963113a1170de795e4b725b84d1e0b4cfd9ec58ce9",
                    "size": 1
                }
            },
            "right": {
                "hash": "e5e27c7f259cb9a773b66fb3675ba1bae0ac36d1c9e9dc59eaaab7a1a0a21c56",
                "size": 2,
                "left": {
                    "hash": "5d9896af338ff832d279efd9fac6694c77118a8a5c42425dac1827ea41f97e2a",
                    "size": 1
                },
                "right": {
                    "hash": "07d046d5fac12b3f82daf5035b9aae86db5adc8275ebfbf05ec83005a4a8ba3e",
                    "size": 1
                }
            }
        },
        "right": {
            "hash": "c3800c31c1335f0c8c3d2b5a461077561ee4693c72407436064708238f5a29ad",
            "size": 2,
            "left": {
                "hash": "85262adf74518bbb70c7cb94cd6159d91669e5a81edf1efebd543eadbda9fa2b",
                "size": 1
            },
            "right": {
                "hash": "d0cfc2e5319b82cdc71a33873e826c93d7ee11363f8ac91c4fa3a2cfcd2286e5",
                "size": 1
            }
        }
    }
}
> python3 checkconsistency.py '["alice", "bob", "carlol", "david"]' '["alice", "bob", "david", "eve", "fred"]'
No
> cat merkle.trees
{
    "old": {
        "hash": "b1833ecfe5a6c8aeae767ac902d2188cd3efd63bc3f9b45a0eb98a6812029198",
        "size": 4,
        "left": {
            "hash": "cb57721dc3aa8df0eef91989560b053a86be98131f45650bd1c3955e0167ef17",
            "size": 2,
            "left": {
                "hash": "2bd806c97f0e00af1a1fc3328fa763a9269723c8db8fac4f93af71db186d6e90",
                "size": 1
            },
            "right": {
                "hash": "81b637d8fcd2c6da6359e6963113a1170de795e4b725b84d1e0b4cfd9ec58ce9",
                "size": 1
            }
        },
        "right": {
            "hash": "e5e27c7f259cb9a773b66fb3675ba1bae0ac36d1c9e9dc59eaaab7a1a0a21c56",
            "size": 2,
            "left": {
                "hash": "5d9896af338ff832d279efd9fac6694c77118a8a5c42425dac1827ea41f97e2a",
                "size": 1
            },
            "right": {
                "hash": "07d046d5fac12b3f82daf5035b9aae86db5adc8275ebfbf05ec83005a4a8ba3e",
                "size": 1
            }
        }
    },
    "new": {
        "hash": "6a01ab792edab953964bf8b868e3f9729c68c591068f658acf6f4b50d995d428",
        "size": 5,
        "left": {
            "hash": "c17d9e1f6a07c0f0a5f939b93255c4a1237c5b24ea8d793241abb6ad12fcaa96",
            "size": 4,
            "left": {
                "hash": "cb57721dc3aa8df0eef91989560b053a86be98131f45650bd1c3955e0167ef17",
                "size": 2,
                "left": {
                    "hash": "2bd806c97f0e00af1a1fc3328fa763a9269723c8db8fac4f93af71db186d6e90",
                    "size": 1
                },
                "right": {
                    "hash": "81b637d8fcd2c6da6359e6963113a1170de795e4b725b84d1e0b4cfd9ec58ce9",
                    "size": 1
                }
            },
            "right": {
                "hash": "2fea8b8d968aa314deff7ac5c6a3351f3b9e0513b6b4e37ee837cb911bf3ef75",
                "size": 2,
                "left": {
                    "hash": "07d046d5fac12b3f82daf5035b9aae86db5adc8275ebfbf05ec83005a4a8ba3e",
                    "size": 1
                },
                "right": {
                    "hash": "85262adf74518bbb70c7cb94cd6159d91669e5a81edf1efebd543eadbda9fa2b",
                    "size": 1
                }
            }
        },
        "right": {
            "hash": "d0cfc2e5319b82cdc71a33873e826c93d7ee11363f8ac91c4fa3a2cfcd2286e5",
            "size": 1
        }
    }
}
> python3 checkconsistency.py '["alice", "bob", "carlol", "david"]' '["alice", "bob", "carlol", "eve", "fred", "davis"]'
No
> cat merkle.trees
{
    "old": {
        "hash": "b1833ecfe5a6c8aeae767ac902d2188cd3efd63bc3f9b45a0eb98a6812029198",
        "size": 4,
        "left": {
            "hash": "cb57721dc3aa8df0eef91989560b053a86be98131f45650bd1c3955e0167ef17",
            "size": 2,
            "left": {
                "hash": "2bd806c97f0e00af1a1fc3328fa763a9269723c8db8fac4f93af71db186d6e90",
                "size": 1
            },
            "right": {
                "hash": "81b637d8fcd2c6da6359e6963113a1170de795e4b725b84d1e0b4cfd9ec58ce9",
                "size": 1
            }
        },
        "right": {
            "hash": "e5e27c7f259cb9a773b66fb3675ba1bae0ac36d1c9e9dc59eaaab7a1a0a21c56",
            "size": 2,
            "left": {
                "hash": "5d9896af338ff832d279efd9fac6694c77118a8a5c42425dac1827ea41f97e2a",
                "size": 1
            },
            "right": {
                "hash": "07d046d5fac12b3f82daf5035b9aae86db5adc8275ebfbf05ec83005a4a8ba3e",
                "size": 1
            }
        }
    },
    "new": {
        "hash": "9232167d7ba7c3e9e396eb501301c3c6f152fa1499b87c6998077b3d0c698b98",
        "size": 6,
        "left": {
            "hash": "c8d2cbbdfb655f85be8b5d8972b37a71e071fd89a25d0e25d48fa0d12bab41ef",
            "size": 4,
            "left": {
                "hash": "cb57721dc3aa8df0eef91989560b053a86be98131f45650bd1c3955e0167ef17",
                "size": 2,
                "left": {
                    "hash": "2bd806c97f0e00af1a1fc3328fa763a9269723c8db8fac4f93af71db186d6e90",
                    "size": 1
                },
                "right": {
                    "hash": "81b637d8fcd2c6da6359e6963113a1170de795e4b725b84d1e0b4cfd9ec58ce9",
                    "size": 1
                }
            },
            "right": {
                "hash": "af0da8e7f810fb7f8cf2688a89ed1136dfc708a601e94483ed5554a1e7dba9be",
                "size": 2,
                "left": {
                    "hash": "5d9896af338ff832d279efd9fac6694c77118a8a5c42425dac1827ea41f97e2a",
                    "size": 1
                },
                "right": {
                    "hash": "85262adf74518bbb70c7cb94cd6159d91669e5a81edf1efebd543eadbda9fa2b",
                    "size": 1
                }
            }
        },
        "right": {
            "hash": "4cf25d75006ae5e0210ba6607b2959b36006e7f76ba6a5bcf566c2316587086c",
            "size": 2,
            "left": {
                "hash": "d0cfc2e5319b82cdc71a33873e826c93d7ee11363f8ac91c4fa3a2cfcd2286e5",
                "size": 1
            },
            "right": {
                "hash": "4458e908dd9a5440ad70b4d0ee13ebe96f0d25bb263b80169b3de5a9a0b90e3d",
                "size": 1
            }
        }
    }
}
```

## Reference

Laurie, B., Langley, A., and E. Kasper, "Certificate Transparency", RFC 6962, DOI 10.17487/RFC6962, June 2013, <https://www.rfc-editor.org/info/rfc6962>.
