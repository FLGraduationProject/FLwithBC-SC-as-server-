// SPDX-License-Identifier: MIT
pragma experimental ABIEncoderV2;

contract Chunk {
    
    struct Codebook {
        uint16 scale_significand;
        int8 scale_exponent;
        uint8 zero_point;
    }
    mapping(uint8 => uint16[]) public arr;


    // mapping(uint16 => uint16[]) public chunks;
    Codebook codebook;
    

    function upload_book(Codebook memory book) public {
        codebook = book;
    }

    function upload_arr(uint8 key, uint16[] memory value) public {
        arr[key] = value;
    }
    
    function download_chunk() public view returns (Codebook memory book) {
        return codebook;
    }
}