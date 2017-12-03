
web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));
addressVoting = '0x0e1864791ed49ebdac0d6bff4b457477c5cc1eb8';
interfaceVoting = '[{"constant":true,"inputs":[{"name":"","type":"bytes32"}],"name":"constituencyDict","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"candidate","type":"bytes32"}],"name":"totalVotesFor","outputs":[{"name":"","type":"uint8"},{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"candidate","type":"bytes32"}],"name":"getCandidateConstituency","outputs":[{"name":"","type":"bool"},{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"candidate","type":"bytes32"}],"name":"validCandidate","outputs":[{"name":"","type":"bool"},{"name":"","type":"string"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"bytes32"}],"name":"votesReceived","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"x","type":"bytes32"}],"name":"bytes32ToString","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"candidateList","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"candidate","type":"bytes32"}],"name":"voteForCandidate","outputs":[{"name":"","type":"bool"},{"name":"","type":"string"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"test","outputs":[{"name":"","type":"bool"},{"name":"","type":"string"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"candidateNames","type":"bytes32[]"},{"name":"constituencies","type":"bytes32[]"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]';
abiVotingContract = JSON.parse(interfaceVoting);
VotingContract = web3.eth.contract(abiVotingContract);
votingContractInstance = VotingContract.at(addressVoting); 

addressAuthentication = '0x8b390ef15ad5cb76bb5a735088825cf90de2ffe0';
interfaceAuthentiation = '[{"constant":false,"inputs":[{"name":"candidate","type":"bytes32"},{"name":"voter","type":"bytes32"}],"name":"checkConstituency","outputs":[{"name":"","type":"bool"},{"name":"","type":"string"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"bytes32"}],"name":"constituencyDict","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"voter","type":"bytes32"}],"name":"isVoteAvailable","outputs":[{"name":"","type":"bool"},{"name":"","type":"string"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"voterList","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"resetVoters","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"candidate","type":"bytes32"},{"name":"voter","type":"bytes32"}],"name":"validVoter","outputs":[{"name":"","type":"bool"},{"name":"","type":"string"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"ping","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"bytes32"}],"name":"votesAvailable","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"x","type":"bytes32"}],"name":"bytes32ToString","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"candidate","type":"bytes32"},{"name":"voter","type":"bytes32"}],"name":"isAuthentic","outputs":[{"name":"","type":"bool"},{"name":"","type":"string"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"voter","type":"bytes32"}],"name":"isVoterExist","outputs":[{"name":"","type":"bool"},{"name":"","type":"string"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"voting","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[{"name":"myList","type":"bytes32[]"},{"name":"constituencies","type":"bytes32[]"},{"name":"addr","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]';
abiAuthenticationContract = JSON.parse(interfaceAuthentiation);
AuthenticationContract = web3.eth.contract(abiAuthenticationContract);
authenticationContractInstance = AuthenticationContract.at(addressAuthentication);

candidates = {"Anuj": "candidate-1", "Dinesh": "candidate-2", "Dushyant": "candidate-3", "ABCD": "candidate-4", "EFGH": "candidate-5", "Modi": "candidate-6"};

function voteForCandidate() {

  candidateName = $("#candidate").val();
  console.log('candidateName:' + candidateName);

  voterName = $("#voter").val();
  console.log('voterName:' + voterName);

  isAuthenticResponse = isAuthenticVoter(candidateName, voterName);
  console.log("isAuthentic:" + isAuthenticResponse);

  if(isAuthenticResponse[0] == false)
  {
    console.log(isAuthenticResponse[1]);
    alert(isAuthenticResponse[1]);
    return;
  }

  console.log("test1"+votingContractInstance.totalVotesFor.call(candidateName));

  votingContractInstance.voteForCandidate(candidateName, {from: web3.eth.accounts[1]}, function() {
    let div_id = candidates[candidateName];
    console.log(div_id);
    $("#" + div_id).html(votingContractInstance.totalVotesFor.call(candidateName)[0].toString());
    console.log(votingContractInstance.totalVotesFor.call(candidateName)[0].toString());
    alert("voting done");
  });
}

$(document).ready(function() {
  candidateNames = Object.keys(candidates);
  for (var i = 0; i < candidateNames.length; i++) {
    let name = candidateNames[i];
    let val = votingContractInstance.totalVotesFor.call(name)[0].toString();
    $("#" + candidates[name]).html(val);
  }
});

function isAuthenticVoter(candidateName, voterName)
{
  isAuthenticResponse = authenticationContractInstance.isAuthentic.call(candidateName, voterName);
  authenticationContractInstance.isAuthentic(candidateName, voterName, {from: web3.eth.accounts[0]}, function(){});
  return isAuthenticResponse;
}

// function resetVoters()
// {
//   authenticationContractInstance.resetVoters({from: web3.eth.accounts[0]}, function(){});
// }