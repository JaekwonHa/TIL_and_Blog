# Java 분석 도구 (jps, jstat, jstack, jmap, jconsole, VisualVM, MAT)

## 목표

이전글들을 통해, Java가 객체를 메모리에 저장하는 방법, JVM의 구조, 가비지 컬렉터의 동작방식 등을 보았습니다.

기반 지식들은 알았는데, 실제로 JVM의 문제가 발생했을때 우리는 어떻게 분석할 수 있을까요? Memory Leak이 의심될때 우리가 사용할 수 있는 CLI, GUI 도구들은 무엇이 있는지, 어떻게 사용하면 좋을지 알아보겠습니다.

> 이전글
> * [java가 메모리를 할당하는 방법 (객체 크기 계산)](https://tangoblog.tistory.com/14)
> * [JVM 알아보기 GC, option, gc.log](https://tangoblog.tistory.com/15)

## Java 관련 도구

`$JAVA_HOME/bin` 디렉토리로 이동해보면 다양한 CLI 도구들도 있고, 설치해서 사용할 수 있는 GUI 도구들도 있습니다. 현재 메모리 상태를 바로 보여준다던가, 스레드 덤프, 힙 덤프를 추출할 수 있는 유용하게 사용할 수 있는 몇가지 툴들을 보겠습니다.

* java -XX:+PrintFlagsFinal
* jps
* jstat
* jstack
* jmap
* jconsole, VisualVM
* Eclipse Memory Analyzer (MAT)

### java -XX:+PrintFlagsFinal -version | grep -iE {OptionName}

JVM Flag들이 현재 어떻게 설정되어있는지 확인해보고 싶을때 사용하는 커맨드입니다.

```shell
$ java -XX:+PrintFlagsFinal -version | grep -iE 'heapsize|permsize|threadstacksize'

     intx CompilerThreadStackSize                   = 0                                   {pd product}
    uintx ErgoHeapSizeLimit                         = 0                                   {product}
    uintx HeapSizePerGCThread                       = 87241520                            {product}
    uintx InitialHeapSize                          := 268435456                           {product}
    uintx LargePageHeapSizeThreshold                = 134217728                           {product}
    uintx MaxHeapSize                              := 4294967296                          {product}
     intx ThreadStackSize                           = 1024                                {pd product}
     intx VMThreadStackSize                         = 1024                                {pd product}
openjdk version "1.8.0_272"
OpenJDK Runtime Environment (AdoptOpenJDK)(build 1.8.0_272-b10)
OpenJDK 64-Bit Server VM (AdoptOpenJDK)(build 25.272-b10, mixed mode)
```

### jps [-v]

JVM 위에서 실행 중인 프로세스를 확인합니다. 실행 중인 Java 프로세스의 VM ID를 확인하는데 유용합니다. Java 커맨드들을 사용할때는 VM ID를 넘겨주어야 합니다.

jps 명령으로 java 프로세스가 보이지 않는다면, 다른 java 프로세스가 root 권한으로 실행된건 아닌지 확인해봐야 합니다.

```shell
$ jps
33457 Jps
```

### jstat

JVM 상태를 모니터링하는 도구입니다. jstack, jmap과는 다르게 서비스에 영향을 주지 않기 때문에 서비스 중인 프로세스에도 사용할 수 있습니다. 프로세스가 실행 후 MinorGC, FullGC가 각각 몇번 발생했는지, heap, metaspace 공간에 대한 정보도 알 수 있습니다.

`jstat -options` 명령어는 어떤 통계를 볼지 선택할 수 있는 인자 list를 볼 수 있습니다.

아래 커맨드는 각 통계에 대해서 각 칼럼의 header를 20라인마다 출력(-h20)하고, 3000ms마다 통계를 출력하는 커맨드입니다. 3번째 출력되는 통계에서 FullGC가 발생합니다.

```shell
$ jstat -gc -h20 44555 3000
 S0C    S1C    S0U    S1U      EC       EU        OC         OU       MC     MU    CCSC   CCSU   YGC     YGCT    FGC    FGCT     GCT   
34944.0 34944.0  0.0   34944.0 279616.0 160556.1  699072.0   198794.6  4864.0 2823.0 512.0  298.2       1    0.478   0      0.000    0.478
34944.0 34944.0  0.0   34944.0 279616.0 160556.1  699072.0   198794.6  4864.0 2823.0 512.0  298.2       1    0.478   0      0.000    0.478
34944.0 34944.0  0.0    0.0   279616.0 225028.8  699072.0   368152.6  4864.0 2826.1 512.0  298.2       1    0.478   1      0.610    1.087

$ jstat -gcutil -h20 48602 3000
  S0     S1     E      O      M     CCS    YGC     YGCT    FGC    FGCT     GCT   
  0.00 100.00  59.40  28.07  58.04  58.24      1    0.408     0    0.000    0.408
  0.00 100.00  59.40  28.07  58.04  58.24      1    0.408     0    0.000    0.408
  0.00   0.00  78.55  52.66  58.10  58.24      1    0.408     1    0.616    1.024

$ jstat -gccapacity -h20 48869 3000
 NGCMN    NGCMX     NGC     S0C   S1C       EC      OGCMN      OGCMX       OGC         OC       MCMN     MCMX      MC     CCSMN    CCSMX     CCSC    YGC    FGC 
349504.0 349504.0 349504.0 34944.0 34944.0 279616.0   699072.0   699072.0   699072.0   699072.0      0.0 1056768.0   4864.0      0.0 1048576.0    512.0      1     0
349504.0 349504.0 349504.0 34944.0 34944.0 279616.0   699072.0   699072.0   699072.0   699072.0      0.0 1056768.0   4864.0      0.0 1048576.0    512.0      1     0
349504.0 349504.0 349504.0 34944.0 34944.0 279616.0   699072.0   699072.0   699072.0   699072.0      0.0 1056768.0   4864.0      0.0 1048576.0    512.0      1     1
```

### jstack

스레드 전체 덤프를 출력합니다. JVM 내부에서 각 Thread 객체마다 Thread.getAllStackTraces, Thread.dumpStack()을 호출한 것과 동일합니다. 시스템에 따라 Hang이 발생할 수 있습니다.

`kill -3 PID` 명령어를 주면 어플리케이션의 스레드 덤프가 표준 출력에 출력됩니다. `-l` 옵션을 주면 잠금 세부 사항도 확인할 수 있습니다.

> 스레드 덤프 분석: https://fastthread.io/ft-index.jsp

```shell
$ jstack -l 49394
2021-01-21 21:26:37
Full thread dump OpenJDK 64-Bit Server VM (25.272-b10 mixed mode):

"Attach Listener" #10 daemon prio=9 os_prio=31 tid=0x00007fd317073800 nid=0x3007 waiting on condition [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE

   Locked ownable synchronizers:
        - None

"Service Thread" #9 daemon prio=9 os_prio=31 tid=0x00007fd31885a000 nid=0x3a03 runnable [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE

   Locked ownable synchronizers:
        - None

"C1 CompilerThread3" #8 daemon prio=9 os_prio=31 tid=0x00007fd31883f000 nid=0x4b03 waiting on condition [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE

   Locked ownable synchronizers:
        - None

"C2 CompilerThread2" #7 daemon prio=9 os_prio=31 tid=0x00007fd317810000 nid=0x3803 waiting on condition [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE

   Locked ownable synchronizers:
        - None

"C2 CompilerThread1" #6 daemon prio=9 os_prio=31 tid=0x00007fd319809000 nid=0x4d03 waiting on condition [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE

   Locked ownable synchronizers:
        - None

"C2 CompilerThread0" #5 daemon prio=9 os_prio=31 tid=0x00007fd31883e800 nid=0x4f03 waiting on condition [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE

   Locked ownable synchronizers:
        - None

"Signal Dispatcher" #4 daemon prio=9 os_prio=31 tid=0x00007fd318814800 nid=0x5003 runnable [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE

   Locked ownable synchronizers:
        - None

"Finalizer" #3 daemon prio=8 os_prio=31 tid=0x00007fd318813800 nid=0x2b03 in Object.wait() [0x00007000030ee000]
   java.lang.Thread.State: WAITING (on object monitor)
        at java.lang.Object.wait(Native Method)
        - waiting on <0x00000007a9ac88e0> (a java.lang.ref.ReferenceQueue$Lock)
        at java.lang.ref.ReferenceQueue.remove(ReferenceQueue.java:144)
        - locked <0x00000007a9ac88e0> (a java.lang.ref.ReferenceQueue$Lock)
        at java.lang.ref.ReferenceQueue.remove(ReferenceQueue.java:165)
        at java.lang.ref.Finalizer$FinalizerThread.run(Finalizer.java:216)

   Locked ownable synchronizers:
        - None

"Reference Handler" #2 daemon prio=10 os_prio=31 tid=0x00007fd318810800 nid=0x2103 in Object.wait() [0x0000700002feb000]
   java.lang.Thread.State: WAITING (on object monitor)
        at java.lang.Object.wait(Native Method)
        - waiting on <0x00000007a9ac8a98> (a java.lang.ref.Reference$Lock)
        at java.lang.Object.wait(Object.java:502)
        at java.lang.ref.Reference.tryHandlePending(Reference.java:191)
        - locked <0x00000007a9ac8a98> (a java.lang.ref.Reference$Lock)
        at java.lang.ref.Reference$ReferenceHandler.run(Reference.java:153)

   Locked ownable synchronizers:
        - None

"main" #1 prio=5 os_prio=31 tid=0x00007fd31800d800 nid=0x1603 waiting on condition [0x0000700002de5000]
   java.lang.Thread.State: TIMED_WAITING (sleeping)
        at java.lang.Thread.sleep(Native Method)
        at Application.main(Application.java:31)

   Locked ownable synchronizers:
        - None

"VM Thread" os_prio=31 tid=0x00007fd31a008800 nid=0x2207 runnable 

"VM Periodic Task Thread" os_prio=31 tid=0x00007fd31a00a800 nid=0x4903 waiting on condition 

JNI global references: 5
```

### jmap

힙 덤프를 발생시켜서 어떤 객체가 어떤 값을 가지고 있는지 저장합니다. stop-the-world를 발생시키므로 서비스 중인 프로세스에는 반드시 필요한 상황에서만 사용해야 합니다.

jmap 커맨드로 생성한 힙 덤프파일은 이후 설명할 MAT에서 업로드해 분석할 수 있습니다.

```shell
jmap -dump:format=b,file=heap.hprof 50690
```

콘솔에서 heap dump의 결과를 바로 출력하고자 한다면 아래 2가지 명령어를 사용할 수 있습니다.

* jmap -histo 50690
  * FullGC가 일어나지 않음. GC가 일어나지 않기 때문에 GC 대상이 되는 객체들도 결과에 포함됨
* jmap -histo:live 50690
  * FullGC가 일어남. 서비스 중인 프로세스에는 신중하게 사용해야함
  
이때 클래스 이름 중에서 이상한 이름들이 있는데 뜻은 아래와 같습니다.
```shell
[C is a char[]
[S is a short[]
[I is a int[]
[B is a byte[]
[[I is a int[][]
```

### jconsole, VisualVM

java 모니터링 도구로서 기본적으로 제공해주는 툴이 jconsole, VisualVM 인데, VisualVM은 jconsole보다 좀 더 많은 프로파일링 정보를 제공합니다. Mac 환경 기준으로 jconsole은 JDK 설치시에 자동으로 설치되지만, VisualVM은 자동으로 설치되지 않았습니다. (윈도우는 자동 설치된다고 합니다.)

> VisualVM 다운로드: https://visualvm.github.io/download.html

jconsole과 VisuaVM 각각으로 Intellij 프로그램을 열어보겠습니다.

jconsole 명령어를 실행시 로컬 프로세스 혹은 외부 프로세스에 연결할 수 있고, CPU, Heap, Metaspace, Classes, Threads 항목을 실시간으로 모니터링 할 수 있고, GC를 강제로 실행시키는 것도 가능합니다.

![img](https://github.com/JaekwonHa/TIL_and_Blog/blob/master/blog/assets/java_tool_jconsole.png?raw=true)

다음은 VisualVM 입니다. jconsole에서 제공해주는 기능은 다 제공해준다고 보면 되고, 추가로 Heap Dump, Thread Dump 추출, 분석과 플러그인을 추가해서 사용하는게 가능합니다.

![img](https://github.com/JaekwonHa/TIL_and_Blog/blob/master/blog/assets/java_tool_visualvm_1.png?raw=true)

VisualGC 라는 플러그인을 설치하면 GC와 여러 정보를 실시간으로 시각화해서 보여주는데, Intellij에서 문자를 쓰거나, 지울때마다 Eden 영역이 늘어나고 MinorGC가 발생하면서 Eden 영역이 클리어되는 것을 볼 수 있습니다.

![img](https://github.com/JaekwonHa/TIL_and_Blog/blob/master/blog/assets/java_tool_visualvm_2.png?raw=true)

![img](https://github.com/JaekwonHa/TIL_and_Blog/blob/master/blog/assets/java_tool_visualvm_3.png?raw=true)

### Heap Memory 분석 도구 Eclipse Memory Analyzer (MAT)

> MAT 다운로드: https://www.eclipse.org/mat/

오픈소스 메모리 분석 도구입니다. Memory Leak 리포트나 생성된 객체, 차지하는 메모리들을 잘 보여주고 있어서 heap memory, Memory Leak 분석에 유용한 툴입니다.

Heap Dump 파일 오픈시에 파일이 너무 크면 MAT 프로그램이 out-of-memory 발생할 수 있습니다. 

```
An internal error occurred during: 
"Parsing heap dump from **.Java heap space
```

Mac(Catalina 10.15.7)에서는 아래와 같이 프로그램 실행시에 메모리를 좀 늘려서 실행해주면 해결되었습니다.

```
cd /Applications/mat.app/Contents/MacOS
./MemoryAnalyzer -vmargs -Xmx5g -XX:-UseGCOverheadLimit
```

production 서버에서 jmap 명령어로 Heap Dump 파일을 추출 후, 로컬로 가져와서 Open 해줍니다.

![img](https://github.com/JaekwonHa/TIL_and_Blog/blob/master/blog/assets/java_tool_mat_3.png?raw=true)

Report들을 추가할 수 있는데, Memory Leak Report를 추가해줍니다.

![img](https://github.com/JaekwonHa/TIL_and_Blog/blob/master/blog/assets/java_tool_mat_1.png?raw=true)

![img](https://github.com/JaekwonHa/TIL_and_Blog/blob/master/blog/assets/java_tool_mat_2.png?raw=true)

Heap Dump 추출 시점에 어떤 객체가 가장 많이 생성되어 있는지, Memory Leak 을 발생시키고 있는 것으로 의심되는 객체들의 리스트를 알 수 있습니다.

## 정리

* jps, jstat: 서버에 직접 접근이 가능하고, 간단하게 콘솔에서 프로세스의 상태를 모니터링
* jconsole, VisualVM: 리모트로 프로세스 접속이 가능하고, 실시간으로 모니터링, 시각화 필요
* jstack, 스레드 덤프 분석 웹사이트들: 애플리케이션이 느리게 동작한다거나, 데드락이 의심될때 스레드 상태를 분석
* jmap, MAT: Memory Leak이 의심되어서 프로세스를 검사해보고 싶다면, jmap 명령어로 힙덤프 파일을 추출하고 MAT 프로그램으로 분석. VisualVM 으로 프로세스를 모니터링하면서 일정 시간 동안 메모리가 어떻게 변하는지 보는 것도 좋지만 과거 데이터까지 보면서 각종 메트릭들의 변화 추이를 보고 싶다면 별도의 모니터링 시스템을 구축 필요. (Prometheus와 같은)

## 참고

* https://stackoverflow.com/questions/9819905/eclipse-memory-analyser-but-always-shows-an-internal-error-occurred/39570003
* https://blog.naver.com/pcmola/222038466393
