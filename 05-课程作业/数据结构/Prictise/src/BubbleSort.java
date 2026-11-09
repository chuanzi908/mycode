public class BubbleSort {
    // 冒泡排序
    public static void bubbleSort(int[] arr){
        int len = arr.length;
        // 外层控制排序轮数
        for(int i = 0; i < len - 1; i++){
            // 内层两两比较
            for(int j = 0; j < len - 1 - i; j++){
                // 前面数字大于后面，交换
                if(arr[j] > arr[j+1]){
                    int temp = arr[j];
                    arr[j] = arr[j+1];
                    arr[j+1] = temp;
                }
            }
        }
    }

    // 测试主方法
    public static void main(String[] args) {
        int[] nums = {5,2,9,1,5,6};
        bubbleSort(nums);
        // 遍历输出结果
        for (int num : nums) {
            System.out.print(num+" ");
        }
    }
}
