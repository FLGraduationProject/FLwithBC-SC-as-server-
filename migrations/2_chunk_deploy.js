const Chunk = artifacts.require("./chunk.sol");

module.exports = function (deployer) {
  deployer.deploy(Chunk);
};