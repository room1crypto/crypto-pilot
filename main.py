const { ethers } = require("ethers");
const fs = require("fs");

// Завантаження приватного ключа з файлу
const senderPrivateKey = fs.readFileSync("sepolia/private_keys.txt", "utf8").trim();

// RPC URL для мережі Sepolia
const sepoliaRpcUrl = "https://rpc.ankr.com/eth_sepolia";
const provider = new ethers.JsonRpcProvider(sepoliaRpcUrl);

// Адреса контракту моста
const bridgeContractAddress = "0x000000000000000000000000000000000000800A"; // Замінити на реальну адресу

// ABI контракту моста (залежить від контракту)
const bridgeAbi = [
  "function bridgeToAbstract(address recipient, uint256 amount) public",
];

// Створення гаманця
const wallet = new ethers.Wallet(senderPrivateKey, provider);

// Підключення до контракту
const bridgeContract = new ethers.Contract(bridgeContractAddress, bridgeAbi, wallet);

// Функція для виконання Bridge
async function bridgeToAbstract(recipient, amountInEth) {
  try {
    console.log(`Starting bridge to Abstract network...`);

    // Переведення суми в Wei
    const amountInWei = ethers.parseUnits(amountInEth.toString(), "ether");

    // Виклик функції bridgeToAbstract
    const tx = await bridgeContract.bridgeToAbstract(recipient, amountInWei, {
      gasLimit: 300000, // Ліміт газу (залежить від контракту)
    });

    console.log("Transaction sent. Waiting for confirmation...");
    const receipt = await tx.wait();

    console.log(`Transaction confirmed in block: ${receipt.blockNumber}`);
    console.log(`Transaction hash: ${tx.hash}`);
  } catch (error) {
    console.error("Error occurred during the bridge process:", error.message);
  }
}

// Виклик функції bridgeToAbstract
const recipientAddress = "0x90f857c37ffe2bb69d0b2cb50307e3f91b7a521a"; // Замінити на адресу отримувача
const amountToBridge = 0.1; // Сума в ETH

bridgeToAbstract(recipientAddress, amountToBridge);
