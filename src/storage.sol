// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.8.0;

contract Storage {
    
    struct Chunk {
        uint8[] arr;
        uint16 scale_significand;
        int8 scale_exponent;
        uint8 zero_point;
    }

    mapping(uint16 => Chunk) public chunks;
    

    function upload_chunk(uint8 chunk_num, uint8[] memory arr, uint16 scale_significand, int8 scale_exponent, uint8 zero_point) public {
        chunks[chunk_num].arr = arr;
        chunks[chunk_num].scale_significand = scale_significand;
        chunks[chunk_num].scale_exponent = scale_exponent;
        chunks[chunk_num].zero_point = zero_point;
    }
    
    function download_chunk(uint8 chunk_num) public view returns (uint8[] memory arr, uint16 scale_significand, int8 scale_exponent, uint8 zero_point) {
        Chunk memory chunk = chunks[chunk_num];
        return (chunk.arr, chunk.scale_significand, chunk.scale_exponent, chunk.zero_point);
    }
}