from web3 import Web3
from solcx import compile_standard

# Connect to the local Ethereum blockchain (e.g., Ganache)
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

# Check if connected to Ethereum node
if not w3.isConnected():
    print("Not connected to Ethereum node.")
    exit()

# Set the default account (the one that will deploy the contract)
w3.eth.default_account = w3.eth.accounts[0]

# Solidity source code
solidity_source_code = """
pragma solidity ^0.8.0;

contract SimpleToken {
    string public name = "SimpleToken";
    string public symbol = "STKN";
    uint256 public totalSupply = 1000000;
    uint8 public decimals = 18;
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }

    function transfer(address _to, uint256 _value) public returns (bool success) {
        require(balanceOf[msg.sender] >= _value, "Insufficient balance");
        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;
        return true;
    }
}
"""

# Compile the Solidity contract
compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {
        "SimpleToken.sol": {
            "content": solidity_source_code
        }
    },
    "settings": {
        "outputSelection": {
            "*": {
                "*": ["abi", "metadata", "evm.bytecode"]
            }
        }
    }
})

# Extract the ABI and bytecode from the compiled contract
abi = compiled_sol['contracts']['SimpleToken.sol']['SimpleToken']['abi']
bytecode = compiled_sol['contracts']['SimpleToken.sol']['SimpleToken']['evm']['bytecode']['object']

# Deploy the contract
SimpleToken = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = SimpleToken.constructor().transact()
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
contract_address = tx_receipt['contractAddress']

# Interact with the deployed contract
simple_token = w3.eth.contract(address=contract_address, abi=abi)
print("Token name:", simple_token.functions.name().call())
