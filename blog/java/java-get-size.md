# java가 메모리를 할당하는 방법 (객체 크기 계산)

## 개요

C/C++의 sizeof() 함수가 있는 것과 달리 Java에서는 Object 크기를 정확하게 측정할 수 있는 방법이 없습니다.

메모리상에 대규모의 데이터를 Cache용도로 저장하여 최대한 성능을 향상시키고자 하는 상황 등에서는 저장하고자 하는 Object 크기를 측정해보는게 굉장히 중요합니다.

이런 요구사항 속에서 어떻게 Java의 Object 크기를 최대한 정확하게 측정할 수 있을지 알아보겠습니다.

아래부터 설명드리는 모든 내용은 JVM 아키텍처와 버전에 따라서 다를 수 있습니다.

## Primitive type

> [primitive type Size 참고](https://www.w3schools.com/java/java_data_types.asp)

* 공식적인 size를 가지고 있습니다. 
* null 값이 존재하지 않습니다.
* wrapper class가 있습니다.
* primitive typye 변수는 thread의 stack memory에 저장됩니다.

type마다 크기가 고정되어 있지만, JVM은 data를 저장할때 언제든지 패딩값이나 오버헤드를 추가할 수 있습니다.

특히 boxed type, array, String 혹은 다차원 array를 비롯한 다른 컨테이너들에는 어느정도의 오버 헤드를 추가하기 때문에 메모리 비용이 예상보다 많이 들 수 있습니다. 예를 들어 int primitive type (4 bytes)은 16 bytes를 사용하는 Integer 객체와 비교하면 300%의 메모리 오버 헤드가 있습니다.

## Object

Hotspot JVM에서 heap 메모리에 저장되는 object는 다음과 같은 특성을 가집니다.

* housekeeping 정보로 구성된 12 bytes의 object header 공간이 있습니다.
  * Class Object (32 bits): 클래스 정보에 대한 포인터
  * Flags (32 bits): 객체의 상태를 설명하는 플래그 모음 (hash-code가 있는지, array인지 등)
  * Lock (32 bits): 동기화 정보, 동기화 잠금 여부
* primitive fields는 각자 정해진 크기만큼 차지합니다.
* reference fields는 4 bytes를 차지합니다. 
* array 배열은 16 bytes가 필요합니다. object 공간 12 bytes + array length 공간 4 bytes
* object 크기는 항상 8의 배수만큼의 byte 공간을 차지합니다. '8-byte alignment', 'object alignment' 라고 합니다. 8의 배수만큼의 byte 공간을 맞춰주기 위해 padding 공간을 붙여줍니다.

![img](https://github.com/JaekwonHa/TIL_and_Blog/blob/master/blog/assets/java_get_size_1.png?raw=true)

> 출처: https://www.slideshare.net/jaxLondonConference/from-java-code-to-java-heap-understanding-the-memory-usage-of-your-app-chris-bailey-ibm-27886078

## Object, Integer, Long, , String 크기 비교

> 타입별 크기 비교 코드 출처: https://www.infoworld.com/article/2077496/java-tip-130--do-you-know-your-data-size-.html

`1.8.0_272, x86_64: "AdoptOpenJDK 8"` 환경에서 타입별 크기를 계산했습니다.

- Object: 16 bytes
  - 12(header) + 4(padding)
- Integer: 16 bytes
  - 12(header) + 4(int)
- Long: 24 bytes
  - 12(header) + 8(long) + 4(padding)
  
Object, Integer, Long 타입의 경우 위에서 설명드린 내용으로 크기를 예상해볼 수 있었습니다.

## arrays

array도 object 타입의 일종입니다. 특히 중요한 것은 다차원 array의 경우 array들의 array라는 것입니다. 예를 들면 2차원 배열은 각각의 요소들이 1차원 배열들로 구성되어있습니다. 이로 인해 나타나는 변화는 아래와 같습니다.

- byte[256]: 272 bytes
- byte[128][1]: 3600 bytes
- int[256]: 1040 bytes
- int[128][1]: 3600 bytes
  
다차원 배열의 경우 꽤 놀라운 결과가 나왔는데, capacity는 동일한 1차원 배열과 2차원 배열의 크기가 눈에 띄게 차이나고 있습니다.

앞선 설명을 다시 생각해봅시다. byte[dim1][dim2] 라고 선언되었다면, 모든 중첩된 byte[dim2] 배열들은 각각의 array 공간을 가집니다. 따라서 각각의 중첩된 배열들이 모두 16 bytes씩의 array 공간에 대한 오버헤드가 발생합니다.

이제 각 결과를 분해해서 생각해보면 다음과 같습니다.

- byte[256]: 272 bytes
  - 12(header) + 256 * 1(byte type size) + 4(padding) = 272
- byte[128][2]: 3600 bytes
  - 바깥 배열
    - 12(header)+4(length)+128 * 4(reference type size) = 528
  - 안쪽 배열
    - 128 * ( 12(header) + 4(length) + 2 * 1(byte type size) + 6(padding) ) = 3072
- int[256]: 1040 bytes
  - 12(header) + 256 * 4(int type size) + 4(padding) = 1040
- int[128][2]: 3600 bytes
  - 바깥 배열
    - 12(header)+4(length)+128 * 4(reference type size) = 528
  - 안쪽 배열
    - 128 * ( 12(header) + 4(length) + 2 * 4(int type size) ) = 3072
  
int[256] 배열과 int[128][2] 배열은 capacity가 256개로 같지만, Java의 내부 로직에 따라 int[128][2] 배열은 int[256] 배열보다 246%의 메모리 오버헤드가 발생하게 됩니다.

## String

String 크기의 경우 많은 래퍼런스들을 참고했지만, 제 환경과 동일한 결과를 보여주는 래퍼런스를 찾지 못했습니다. (대부분이 오래된 문서여서 JDK 버전이 낮거나, JVM 아키텍처가 달랐습니다.)

제 환경에서 String 크기는 다음과 같았습니다. (`createString()` 메소드를 사용하여 String 객체 생성)

* Empty: 24 bytes
* 1~8 length: 48 bytes
* 9~16 length: 56 bytes
* 17 length: 64 bytes

Empty String이 24 bytes부터 시작해서 1개가 추가될때 48 bytes로 커진 뒤, 8개 단위로 8 bytes씩 커지고 있습니다.

## 가설1. String 객체에는 hash, count, offset, char[] 참조 변수가 있고, char[] 변수가 따로 존재한다.

> 참고 p19 : https://www.slideshare.net/jaxLondonConference/from-java-code-to-java-heap-understanding-the-memory-usage-of-your-app-chris-bailey-ibm-27886078

래퍼런스를 참고하여 String 크기를 계산해보면, 12(header) + 4(hash) + 4(count) + 4(offset) + 4(char[] 참조 변수) = 28 bytes. char[] 변수 크기가 16(array) + n * 2(char type size)입니다.

실제로 Empty String의 크기가 24 bytes인 것을 고려해보면 크기가 너무 크게 나옵니다.

## 가설2. String 객체에는 hash, char[] 변수가 있다.

IDE를 통해 String.java 파일을 직접 열어보면 아래와 같이 선언되어 있습니다.

```java
public final class String implements java.io.Serializable, Comparable<String>, CharSequence {
  /** The value is used for character storage. */
  private final char value[];
  /** Cache the hash code for the string */
  private int hash; // Default to 0
  /** use serialVersionUID from JDK 1.0.2 for interoperability */
  private static final long serialVersionUID = -6849794470754667710L;
    ...
}
```

가설1의 래퍼런스에서 보았던 count, offset 변수는 JDK 1.8 Hotspot 에서는 없는 것 같고, int형 hash 변수, char[]형 value 변수가 있습니다. 그리고 serialVersionUID 변수가 있지만 static 변수이므로 Heap memory 영역에는 영향을 주지 않습니다.

이런 정보를 바탕으로 길이가 8인 String 객체의 크기를 계산해보면, 12(header) + 4(hash) + (16(array) + 8 * 2(char)) = 48 bytes가 계산이 됩니다.

사이즈가 맞긴 하지만 가설을 검증할 수단은 추후에 좀 더 고민을 해봐야 할 것 같고, Empty String의 크기가 왜 24 bytes인지와 capacity가 증가할때마다 길이 8만큼 증가하는게 맞는지도 확인할 수 없었는데, 혹시나 나중에 알게된다면 다시 포스팅해보도록 하겠습니다.

(String 객체의 경우 String pool, 인코딩 방식 등에도 영향을 받을 것 같습니다)

## 정리

그동안 가비지 컬렉터가 알아서 메모리 할당, 정리 등을 해주니 그 내부구조를 자세하게 궁금해하지 않았던 것 같습니다.

Java 개발자로써 Java가 메모리를 할당하는 방법에서부터 JVM의 동작방식, java 파일 빌드과정, 가비지 컬렉터 등의 지식 또한 중요하지 않을까 싶어 정리해보게 되었는데, 생각보다 알게 된 것들이 너무 많아 다른 것들도 좀 정리를 해보려 합니다.

## 참고
- [https://www.baeldung.com/java-size-of-object](https://www.baeldung.com/java-size-of-object)
- [https://www.infoworld.com/article/2077496/java-tip-130--do-you-know-your-data-size-.html](https://www.infoworld.com/article/2077496/java-tip-130--do-you-know-your-data-size-.html)
- [https://jobjava00.github.io/language/java/basic/primitive-type/](https://jobjava00.github.io/language/java/basic/primitive-type/)
- [https://www.javamex.com/tutorials/memory/object_memory_usage.shtml](https://www.javamex.com/tutorials/memory/object_memory_usage.shtml)
- [https://stackoverflow.com/questions/8419860/integer-vs-int-with-regard-to-memory](https://stackoverflow.com/questions/8419860/integer-vs-int-with-regard-to-memory)
- [https://www.javamex.com/tutorials/memory/string_memory_usage.shtml](https://www.javamex.com/tutorials/memory/string_memory_usage.shtml)
- [https://www.slideshare.net/jaxLondonConference/from-java-code-to-java-heap-understanding-the-memory-usage-of-your-app-chris-bailey-ibm-27886078](https://www.slideshare.net/jaxLondonConference/from-java-code-to-java-heap-understanding-the-memory-usage-of-your-app-chris-bailey-ibm-27886078)
