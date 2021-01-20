# JVM 알아보기 GC, option, gc.log

## 목표

자주 쓰는 JVM option들이 어떤 의미인지, gc.log에 남는 값들은 어떻게 해석하면 되는지 알아봅니다.

## GC

우선 JVM에서 메모리 영역을 어떻게 관리하고 있는지 알아야 합니다. 모든 내용은 jdk8 기준으로 작성되었습니다.

![img](https://github.com/HaJaeKwon/blog/blob/master/assets/jvm-option-space.png?raw=true)

| 출처: https://code-factory.tistory.com/48

1. Eden
   1. Object가 새로 생성되었을때 Eden 영역에 저장
   2. Eden 영역이 가득차게되면 MinorGC가 발생합니다.
   3. MinorGC 발생 시에 Eden 영역에 있는 Reachable Object들은 S0 혹은 S1 영역으로 이동
2. Survivor 1,2
   1. MinorGC가 발생하면 S0 영역에 있는 Reachable Object들은 S1 영역으로 이동하고, S0 영역은 비워집니다.
   2. MinorGC가 다시 발생하면 S1 영역에 있는 Reachable Object들은 S0 영역으로 이동하고, S1 영역은 비워집니다.
   3. Object들은 Survivor 영역을 이동할때마다 Age가 증가하게되고, 어느정도 Age가 증가하면 Old 영역으로 이동합니다.
2. Old
   1. Old 영역이 가득차게 되면 Full GC가 발생합니다.
   2. Young generation 보다 크게 할당되며 크기가 큰 만큼 GC가 적게 발생하지만, 오래 수행될 수 있습니다.

| 모든 GC는 stop-the-world를 발생시킬 수 있습니다. 참고: https://plumbr.io/blog/garbage-collection/minor-gc-vs-major-gc-vs-full-gc

## JVM option

제가 주로 쓰고 있었던 JVM option은 다음과 같습니다.

* -server
  * 프로세스가 오랜시간 살아있게되는 서버 어플리케이션에 적합한 방법입니다. 반대 방법으로는 -client 옵션이 있습니다.
  * 컴파일시에 client 모드보다 더 많은 최적화 방법들을 사용하기에 어플리케이션 시작시간은 느리지만, 뛰어난 성능을 보장합니다.
* -verbosegc
  * GC가 수행될때 로깅을 남기는 옵션입니다. 지속적으로 GC 정보를 모니터링하고자 할때 유용합니다.
  * 다음 옵션과 동일합니다. -verbose:gc, -XX:+PrintGC(JDK 9부터 deprecated), -Xlog:gc(JDK 9부터 사용)
* -verbose:gc
  * -verbosegc 옵션과 동일합니다. (아무 생각없이 동일한 옵션을 2번 쓰고 있었네요)
* -Xms1g, -Xmx2g
  * Heap Memory의 최대, 최소 크기를 명시적으로 지정합니다. 'g', 'm', 'k' 단위(GB,MB,KB)를 줄 수 있습니다.
  * 성능 향상(GC 빈도와 GC 수행시간 간의 최적화)을 위해서 적절한 Heap Memory를 지정하는 것은 아주 중요합니다.
* -XX:+UseConcMarkSweepGC
  * Concurrent Mark And Sweep 방식의 GC를 사용합니다. 
  * Old generation에서 이뤄지고, GC의 stop-the-world 시간을 최소화하는데 목적을 가진 GC 방식입니다. 응답시간 지연을 최소화하는 목적으로 사용합니다.
  * Object 생성비율이 매우 높거나, GC에 실패하게되면 mark-sweep collector (single 스레드 collector) 방식으로 수행됩니다.
  * 여러 단계로 구성되어있기에 다른 GC 대비 CPU 사용량이 높습니다.
  * Application 스레드와 GC 스레드가 동시에 수행되지만, 일부 단계에서는 stop-the-world 가 발생합니다. ([참고](http://www.javaperformancetuning.com/news/qotm026.shtml))
    1. initial-mark phase (stop-the-world)
       * GC Root와 Young generation에서 참조하는 Old generation Object만 마킹한다.
    2. mark phase (concurrent)
       * 1단계에서 GC 대상이 된 Object들이 참조하는 다른 Object들을 탐색하며 GC 대상인지 추가로 확인한다.
    3. pre-cleaning phase (concurrent)
       * 4단계의 STW 시간을 줄이기 위해 Old generation 영역의 일정 공간을 Card로 나누어 저장한다. ([참고](https://perfectacle.github.io/2019/05/11/jvm-gc-advanced/)) 
    4. re-mark phase (stop-the-world)
       * GC 가 시작된 후 Reachable Object에 변화가 있는지 다시 한번 확인한다.
    5. sweep phase (concurrent)
       * Unreachable Object 들을 제거한다.
    6. reset phase (concurrent)
* -XX:+UseParNewGC
  * Young generation 에서 발생하는 GC 방식을 multi 스레드 방식으로 진행합니다. 
  * stop-the-world 가 발생하지만 single 스레드 방식보다 사용가능한 CPU 수 만큼의 효율이 증가합니다.
* -XX:+CMSParallelRemarkEnabled
  * Young generation 에서 발생하는 Remark 단계를 병렬로 진행합니다.
* -XX:CMSInitiatingOccupancyFraction=80
  * CMS 방식은 Application 스레드와 동시에 GC가 발생하기 때문에 도중에 Old generation 이 꽉차게 되면 실패하고 STW가 발생합니다.
  * 이런 상황을 피하기위해 Old generation이 몇% 찾을때 GC가 수행될지 정할 수 있습니다. (80이면 상당히 높게 설정하고 사용하고 있었네요)
* -XX:+CMSClassUnloadingEnabled
  * 기본적으로 CMS 방식(ConcMarkSweep)은 Permanent 영역에서의 GC를 수행하지 않습니다. GC를 수행할 필요가 있다면 해당 옵션을 통해 활성화할 수 있습니다.
  * Permanent 영역은 클래스와 메소드의 메타데이터를 저장합니다. Groovy와 같은 언어에서는 런타임에 클래스를 정의하는 경우가 있어서 스크립트를 실행할때마다 Permanent 영역에 데이터가 지속적으로 저장될 수 있습니다.
  * Permanent 영역은 jdk8부터 쓰이지 않습니다.
* -XX:+DisableExplicitGC
  * `System.gc()` 메소드를 호출해도 GC가 수행되지 않습니다.
* -XX:+PrintGCDetails
  * GC 수행시에 더 자세한 정보를 출력합니다.
* -XX:+PrintGCTimeStamps
  * JVM이 시작된 시간을 기준으로 GC가 발생한 시간을 출력합니다.
  * 실제 시간을 보고 싶다면 `-XX:+PrintGCDateStamps`을 지정할 수 있습니다.
* -XX:+PrintHeapAtGC
  * GC 발생 전, 후로 heap memory에 대한 요약을 출력합니다.
* -Xloggc:gc.log.2021-01-19
  * GC 로그를 파일로 남길 수 있습니다.

## gc.log

제가 쓰는 옵션 중, GC 로그 형태에 대해 영향을 미치는 옵션은 4가지입니다. 단계별로 gc.log에 남는 형태를 봐보겠습니다.

| 참고 소스코드: https://www.baeldung.com/java-verbose-gc

```shell
# 아래 커맨드로 실행
$ javac Application.java
$ java -XX:+UseSerialGC -Xms1024m -Xmx1024m {추가적인 옵션} Application
```

### -verbose:gc

```shell
Start of program!
[GC (Allocation Failure)  279616K->232467K(1013632K), 0.4490921 secs]
MAP size: 3000000
[Full GC (System.gc())  398559K->368152K(1013632K), 0.5403610 secs]
MAP size: 1000000
End of program!
```

각각의 항목을 살펴보면 아래와 같습니다.

* [GC
  * Minor GC인지, Full GC인지 여부
* (Allocation Failure)
  * GC 발생이유
* 279616K->232467K(1013632K)
  * GC 전 heap memory 총 사용량 -> GC 후 heap memory 총 사용량, 괄호안은 전체 heap memory 크기
  * heap memory = young generation + old generation
* 0.4490921 secs]
  * 소요시간

### -XX:+PrintGCTimeStamps

```shell
Start of program!
0.464: [GC (Allocation Failure)  279616K->235021K(1013632K), 0.4629527 secs]
MAP size: 3000000
1.036: [Full GC (System.gc())  395577K->368152K(1013632K), 0.5298344 secs]
MAP size: 1000000
End of program!
```

### -XX:+PrintGCDetails

```shell
Start of program!
2021-01-21T01:11:38.379-0900: [GC (Allocation Failure) 2021-01-21T01:11:38.379-0900: [DefNew: 279616K->34943K(314560K), 0.4455142 secs] 279616K->232449K(1013632K), 0.4455503 secs] [Times: user=0.36 sys=0.08, real=0.45 secs] 
MAP size: 3000000
2021-01-21T01:11:38.933-0900: [Full GC (System.gc()) 2021-01-21T01:11:38.933-0900: [Tenured: 197505K->368152K(699072K), 0.5354533 secs] 398541K->368152K(1013632K), [Metaspace: 2825K->2825K(1056768K)], 0.5354845 secs] [Times: user=0.49 sys=0.04, real=0.53 secs] 
MAP size: 1000000
End of program!
```

MinorGC일 경우에는 young generation (DefNew) 의 사용량 변화, FullGC일 경우에는 old generation (Tenured) 의 사용량 변화와 Metaspace 사용량 변화가 같이 출력됩니다.

### -XX:+PrintHeapAtGC

```shell
Start of program!
{Heap before GC invocations=0 (full 0):
 def new generation   total 314560K, used 279616K [0x0000000780000000, 0x0000000795550000, 0x0000000795550000)
  eden space 279616K, 100% used [0x0000000780000000, 0x0000000791110000, 0x0000000791110000)
  from space 34944K,   0% used [0x0000000791110000, 0x0000000791110000, 0x0000000793330000)
  to   space 34944K,   0% used [0x0000000793330000, 0x0000000793330000, 0x0000000795550000)
 tenured generation   total 699072K, used 0K [0x0000000795550000, 0x00000007c0000000, 0x00000007c0000000)
   the space 699072K,   0% used [0x0000000795550000, 0x0000000795550000, 0x0000000795550200, 0x00000007c0000000)
 Metaspace       used 2822K, capacity 4486K, committed 4864K, reserved 1056768K
  class space    used 298K, capacity 386K, committed 512K, reserved 1048576K
2021-01-21T01:16:22.738-0900: [GC (Allocation Failure) 2021-01-21T01:16:22.738-0900: [DefNew: 279616K->34943K(314560K), 0.4435960 secs] 279616K->232449K(1013632K), 0.4436250 secs] [Times: user=0.37 sys=0.08, real=0.45 secs] 
Heap after GC invocations=1 (full 0):
 def new generation   total 314560K, used 34943K [0x0000000780000000, 0x0000000795550000, 0x0000000795550000)
  eden space 279616K,   0% used [0x0000000780000000, 0x0000000780000000, 0x0000000791110000)
  from space 34944K,  99% used [0x0000000793330000, 0x000000079554fff8, 0x0000000795550000)
  to   space 34944K,   0% used [0x0000000791110000, 0x0000000791110000, 0x0000000793330000)
 tenured generation   total 699072K, used 197505K [0x0000000795550000, 0x00000007c0000000, 0x00000007c0000000)
   the space 699072K,  28% used [0x0000000795550000, 0x00000007a1630738, 0x00000007a1630800, 0x00000007c0000000)
 Metaspace       used 2822K, capacity 4486K, committed 4864K, reserved 1056768K
  class space    used 298K, capacity 386K, committed 512K, reserved 1048576K
}
MAP size: 3000000
{Heap before GC invocations=1 (full 0):
 def new generation   total 314560K, used 195500K [0x0000000780000000, 0x0000000795550000, 0x0000000795550000)
  eden space 279616K,  57% used [0x0000000780000000, 0x0000000789ccb010, 0x0000000791110000)
  from space 34944K,  99% used [0x0000000793330000, 0x000000079554fff8, 0x0000000795550000)
  to   space 34944K,   0% used [0x0000000791110000, 0x0000000791110000, 0x0000000793330000)
 tenured generation   total 699072K, used 197505K [0x0000000795550000, 0x00000007c0000000, 0x00000007c0000000)
   the space 699072K,  28% used [0x0000000795550000, 0x00000007a1630738, 0x00000007a1630800, 0x00000007c0000000)
 Metaspace       used 2825K, capacity 4486K, committed 4864K, reserved 1056768K
  class space    used 298K, capacity 386K, committed 512K, reserved 1048576K
2021-01-21T01:16:23.289-0900: [Full GC (System.gc()) 2021-01-21T01:16:23.289-0900: [Tenured: 197505K->368152K(699072K), 0.5453973 secs] 393005K->368152K(1013632K), [Metaspace: 2825K->2825K(1056768K)], 0.5454307 secs] [Times: user=0.49 sys=0.05, real=0.55 secs] 
Heap after GC invocations=2 (full 1):
 def new generation   total 314560K, used 0K [0x0000000780000000, 0x0000000795550000, 0x0000000795550000)
  eden space 279616K,   0% used [0x0000000780000000, 0x0000000780000000, 0x0000000791110000)
  from space 34944K,   0% used [0x0000000793330000, 0x0000000793330000, 0x0000000795550000)
  to   space 34944K,   0% used [0x0000000791110000, 0x0000000791110000, 0x0000000793330000)
 tenured generation   total 699072K, used 368152K [0x0000000795550000, 0x00000007c0000000, 0x00000007c0000000)
   the space 699072K,  52% used [0x0000000795550000, 0x00000007abcd60c8, 0x00000007abcd6200, 0x00000007c0000000)
 Metaspace       used 2825K, capacity 4486K, committed 4864K, reserved 1056768K
  class space    used 298K, capacity 386K, committed 512K, reserved 1048576K
}
MAP size: 1000000
End of program!
```

GC 전후에 메모리 사용량 변화가 아주 자세히 출력됩니다. young generation 영역에서 from, to 둘 중 하나는 반드시 비어있고, GC가 발생할 때 마다 eden이 비워지고, old generation에 데이터가 쌓이는 것을 볼 수 있습니다.

## 참고
* [https://www.baeldung.com/java-verbose-gc](https://www.baeldung.com/java-verbose-gc)
* [https://stackoverflow.com/questions/49609051/difference-between-xxprintgc-and-verbosegc](https://stackoverflow.com/questions/49609051/difference-between-xxprintgc-and-verbosegc)
* [https://d2.naver.com/helloworld/6043](https://d2.naver.com/helloworld/6043)
* [https://bcho.tistory.com/157](https://bcho.tistory.com/157)
* [https://mirinae312.github.io/develop/2018/06/04/jvm_gc.html](https://mirinae312.github.io/develop/2018/06/04/jvm_gc.html)
* [https://perfectacle.github.io/2019/05/11/jvm-gc-advanced/](https://perfectacle.github.io/2019/05/11/jvm-gc-advanced/)
* [http://daplus.net/java-jvm-%ED%94%8C%EB%9E%98%EA%B7%B8-cmsclassunloadingenabled%EB%8A%94-%EC%8B%A4%EC%A0%9C%EB%A1%9C-%EB%AC%B4%EC%97%87%EC%9D%84%ED%95%A9%EB%8B%88%EA%B9%8C/](http://daplus.net/java-jvm-%ED%94%8C%EB%9E%98%EA%B7%B8-cmsclassunloadingenabled%EB%8A%94-%EC%8B%A4%EC%A0%9C%EB%A1%9C-%EB%AC%B4%EC%97%87%EC%9D%84%ED%95%A9%EB%8B%88%EA%B9%8C/)
* [https://www.baeldung.com/jvm-parameters](https://www.baeldung.com/jvm-parameters)
