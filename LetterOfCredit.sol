pragma solidity ^0.8.0;

contract LetterOfCredit {
 string public letter;

 constructor() {
    profession = 'Letter of Credit: APPROVED';
}

 function setLetter(string memory _letter) public {
    letter = _letter;
 }

 function myLetter() view public returns (string memory) {
    return letter;
 }
}
