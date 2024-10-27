function findLongestSubarrayWithPerfectSquareSum(arr) {
    let longestSubarray = null;

    for (let i = 0; i < arr.length; i++) {
        for (let j = i; j < arr.length; j++) {
            const subarray = arr.slice(i, j + 1);
            const sum = subarray.reduce((acc, val) => acc + val, 0);
            const sqrt = Math.sqrt(sum);

            if (Number.isInteger(sqrt)) {
                if (
                    !longestSubarray ||
                    subarray.length > longestSubarray.length
                ) {
                    longestSubarray = subarray;
                }
            }
        }
    }

    return longestSubarray;
}

const arr1 = [4, 2, 5, 1, 7, 3, 6];
console.log(findLongestSubarrayWithPerfectSquareSum(arr1))