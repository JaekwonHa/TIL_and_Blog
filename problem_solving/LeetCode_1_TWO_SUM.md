# LeetCode 1. Two Sum

> https://leetcode.com/problems/two-sum/

## 문제 이해

* input / output
  * input: int array, int
  * output: 정답쌍의 index
* 내용
  * 첫번째로 주어진 int 형 배열 속에서 서로 다른 두 수를 더해 두번째로 주어진 수가 되는 쌍의 index를 반환한다
  * 제약조건
    * 정답은 유일하다
    * 같은 수를 2번 사용할 수 없다
* 의문
  * input 배열의 크기는 얼마나 크게 들어올까 ?
  * 0과 음수도 input으로 들어올 수 있을까 ?
  * 같은 수가 2번 이상 들어올 수 있을까 ?

## O(N^2)

broute-force 방법으로 접근하면 얼마나 걸릴까요?

간단하게 이중 loop를 수행한다면 N^2 의 시간복잡도로 해결 가능합니다.

첫번째 수(i) 를 고르고 i+1 번째 수부터 두번째 수(j) 를 고른 뒤 두개의 합이 target 이 되는지 확인합니다.

```python
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        for i in range(len(nums)):
            for j in range(i+1, len(nums)):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return [0, 1]
```

**Accepted !**

간단하지만 5976ms로는 하위 8%에 속하는 정답이네요. 개선할 여지가 있어 보입니다.

## O(N)

`x + y = z` 가 이 문제를 관통하는 수식처럼 보입니다.

주어진 x, y 후보군 중에서 두개를 더해 z 가 되는 후보군을 찾아라.

...

변수가 x, y 두개나 되어 O(N) 으로 줄이는 것이 어려워 보이지만..수식을 뒤집어서 생각해보면 `z - x = y` 로 생각해볼 수 있습니다.

x, y 는 정해지지 않았지만 z 는 정해진 숫자이기에 이중 loop 를 돌지 않아도 될 것 같습니다.

우리는 정해진 z 에서 x 를 하나씩 빼보며 y 가 있는지만 확인해보면 되겠고 y 가 있는지 O(1) 에 확인하기 위해서 hashmap 을 사용하면 됩니다.

```python
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        hash = {nums[i]: i for i in range(0, len(nums))}
        for i in range(len(nums)):
            if hash.get(target - nums[i]) is not None:
                return [i, hash.get(target - nums[i])]
        return [0, 1] #default (문제의 조건을 만족한다면 발생하지 않음)
```

**Wrong Answer !**

## 예외상황 처리

* input 배열의 크기는 얼마나 크게 들어올까 ?
  * N^2 으로도 통과는 했으니 굳이 고민할 필요는 없어 보입니다.
* 0과 음수도 input으로 들어올 수 있을까 ?
  * 0, 음수도 input 으로 들어올 수 있어서 target - nums[i] >= target 이 되는 경우를 고민해봐야 합니다.
* 같은 수가 2번 이상 들어올 수 있을까 ?
  * 같은 수가 2번 이상 들어올 수 있습니다. 하지만 문제의 조건에서 **답이 유일**하다고 했고 나중에 들어온 수가 hashmap을 덮어써버리기에 답을 도출하는데는 문제가 없습니다.
* 같은 수가 2번 쓰이는 경우가 있을까 ?
  * 문제를 풀면서 발견한 처리해야 하는 예외 상황입니다.
  * `input: [3,2,4], 6` 같은 경우에 `3`이 2번 쓰이면서 `6`을 만들 수 있습니다. 이런 경우를 제거해줘야 합니다.
  * `hash.get(target - nums[i]) != i:`

```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        hash = {nums[i]: i for i in range(0, len(nums))}
        for i in range(len(nums)):
            if hash.get(target - nums[i]) is not None and hash.get(target - nums[i]) != i:
                return [i, hash.get(target - nums[i])]
        return [0, 1]
```

52ms로 단축되어 문제에서 바라는 시간복잡도를 만족시킨 것 같습니다.
