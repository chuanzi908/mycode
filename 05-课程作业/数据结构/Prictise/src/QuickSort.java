public class QuickSort {
    public static void quickSort(int[] arr,int left,int right){
        if(left >= right) return;
        int i = left,j = right;
        int pivot = arr[left];//基准值
        while(i < j){
            while(i<j && arr[j]>=pivot) j--;
            arr[i] = arr[j];
            while(i<j && arr[i]<=pivot) i++;
            arr[j] = arr[i];
        }
        arr[i] = pivot;
        quickSort(arr,left,i-1);
        quickSort(arr,i+1,right);
    }
    public static void main(String[] args) {
        int[] a = {3,1,4,2,5};
        quickSort(a,0,a.length-1);
        for(int num:a) System.out.print(num+" ");
    }
}