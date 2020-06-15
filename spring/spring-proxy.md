# Spring JDK Dynamic Proxy vs CGLIB 차이점

회사에 입사 후 서비스 중인 Spring 프로젝트들의 코드를 보면 구현체가 하나이지만 인터페이스를 같이 정의해둔 Service 클래스들을 볼 수 있었습니다.

그 당시에는 왜 굳이 인터페이스도 같이 만들어줘야 하는지, (Spring 2.X 기준으로) 이제는 왜 같이 안만들어줘도 되는지 몰랐지만, 이제 알게되어 정리를 해봅니다.

## Proxy 객체

Spring IoC 컨테이너에서는 내부적으로 빈에 대한 Proxy 객체를 생성하여 관리하고 있습니다. 

대표적으로 @Async, @Transaction 어노테이션을 사용하게 되면 Proxy 객체가 생성되고, 해당 메소드를 호출하게 되면 실제로는 Proxy 객체의 메소드가 호출되어 비동기나 트랜잭션 로직을 수행하게 됩니다.

이때 Proxy 객체를 생성하는 방법은 JDK Dynamic Proxy 방법과 CGLIB 방법이 있고, 이 둘의 가장 큰 차이점은 아래와 같습니다.

* JDK Dynamic Proxy: 인터페이스를 활용
* CGLIB: 상속을 활용. class, method 에 final 선언이 불가능

예전에는 CGLIB이 기본 의존성에 포함되지 않아서 따로 의존성을 추가해주는게 아니라면 인터페이스가 같이 정의되어야 JDK Dynamic Proxy 방법을 통해 Proxy 객체를 생성할 수 있었습니다.

하지만 지금은 Spring-Core에 CGLIB이 기본 의존성으로 들어오게 되면서 인터페이스가 없으면 자동으로 CGLIB 방식으로 Proxy 객체를 생성해주게 되었습니다.

이를 확인하기 위한 코드를 작성해보겠습니다.

## JDK Dynamic Proxy 방식
```java
@EnableAsync
@SpringBootApplication
public class DemoApplication implements CommandLineRunner {

    @Autowired
    ApplicationContext applicationContext;

    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }

    @Override
    public void run(String... args) throws Exception {
        UserService userService = applicationContext.getBean(UserService.class);
        System.out.println(userService.getClass());
    }
}

public interface UserService {

    public void getUser();
}

@Service
public class DefaultUserService implements UserService {

    @Async
    @Override
    public void getUser() {
    }
}
```

```shell script
  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/
 :: Spring Boot ::        (v2.3.1.RELEASE)

2020-06-14 18:00:23.011  INFO 19686 --- [           main] com.example.demo.DemoApplication         : Starting DemoApplication on hajaegwonuiMBP with PID 19686 (/Users/jaekwon/workspace/playgroud/demo/build/classes/java/main started by jaekwon in /Users/jaekwon/workspace/playgroud/demo)
2020-06-14 18:00:23.014  INFO 19686 --- [           main] com.example.demo.DemoApplication         : No active profile set, falling back to default profiles: default
2020-06-14 18:00:23.779  INFO 19686 --- [           main] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat initialized with port(s): 8080 (http)
2020-06-14 18:00:23.786  INFO 19686 --- [           main] o.apache.catalina.core.StandardService   : Starting service [Tomcat]
2020-06-14 18:00:23.786  INFO 19686 --- [           main] org.apache.catalina.core.StandardEngine  : Starting Servlet engine: [Apache Tomcat/9.0.36]
2020-06-14 18:00:23.839  INFO 19686 --- [           main] o.a.c.c.C.[Tomcat].[localhost].[/]       : Initializing Spring embedded WebApplicationContext
2020-06-14 18:00:23.839  INFO 19686 --- [           main] w.s.c.ServletWebServerApplicationContext : Root WebApplicationContext: initialization completed in 789 ms
2020-06-14 18:00:23.980  INFO 19686 --- [           main] o.s.s.concurrent.ThreadPoolTaskExecutor  : Initializing ExecutorService 'applicationTaskExecutor'
2020-06-14 18:00:24.137  INFO 19686 --- [           main] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat started on port(s): 8080 (http) with context path ''
2020-06-14 18:00:24.146  INFO 19686 --- [           main] com.example.demo.DemoApplication         : Started DemoApplication in 1.433 seconds (JVM running for 1.974)
class com.sun.proxy.$Proxy52
```

## CGLIB 방식
```java
@EnableAsync
@SpringBootApplication
public class DemoApplication implements CommandLineRunner {

    @Autowired
    ApplicationContext applicationContext;

    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }

    @Override
    public void run(String... args) throws Exception {
        UserService userService = applicationContext.getBean(UserService.class);
        System.out.println(userService.getClass());
    }
}

@Service
public class UserService {

    @Async
    public void getUser() {
    }
}
```

```shell script
  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/
 :: Spring Boot ::        (v2.3.1.RELEASE)

2020-06-14 18:01:53.546  INFO 19694 --- [           main] com.example.demo.DemoApplication         : Starting DemoApplication on hajaegwonuiMBP with PID 19694 (/Users/jaekwon/workspace/playgroud/demo/build/classes/java/main started by jaekwon in /Users/jaekwon/workspace/playgroud/demo)
2020-06-14 18:01:53.548  INFO 19694 --- [           main] com.example.demo.DemoApplication         : No active profile set, falling back to default profiles: default
2020-06-14 18:01:54.386  INFO 19694 --- [           main] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat initialized with port(s): 8080 (http)
2020-06-14 18:01:54.394  INFO 19694 --- [           main] o.apache.catalina.core.StandardService   : Starting service [Tomcat]
2020-06-14 18:01:54.394  INFO 19694 --- [           main] org.apache.catalina.core.StandardEngine  : Starting Servlet engine: [Apache Tomcat/9.0.36]
2020-06-14 18:01:54.451  INFO 19694 --- [           main] o.a.c.c.C.[Tomcat].[localhost].[/]       : Initializing Spring embedded WebApplicationContext
2020-06-14 18:01:54.451  INFO 19694 --- [           main] w.s.c.ServletWebServerApplicationContext : Root WebApplicationContext: initialization completed in 858 ms
2020-06-14 18:01:54.603  INFO 19694 --- [           main] o.s.s.concurrent.ThreadPoolTaskExecutor  : Initializing ExecutorService 'applicationTaskExecutor'
2020-06-14 18:01:54.761  INFO 19694 --- [           main] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat started on port(s): 8080 (http) with context path ''
2020-06-14 18:01:54.770  INFO 19694 --- [           main] com.example.demo.DemoApplication         : Started DemoApplication in 1.627 seconds (JVM running for 2.228)
class com.example.demo.UserService$$EnhancerBySpringCGLIB$$41ed43c
```

## 결론

간단한 테스트를 위해 CommandLineRunner와 @Async를 활용했고, 각각의 결과가 `class com.sun.proxy.$Proxy52`, `class com.example.demo.UserService$$EnhancerBySpringCGLIB$$41ed43c` 를 출력하는 걸 볼 수 있습니다.

인터페이스가 있으면 JDK Dynamic Proxy 방식으로 Proxy 객체가 생성되고, 없으면 CGLIB 방식으로 생성됨을 확인할 수 있습니다.

이런 확인을 통해서 CGLIB이 기본 의존성에 들어와있지 않던 과거 버전 Spring에서는 인터페이스 선언을 해주지 않으면 Proxy 객체를 생성할 수 없어서 인터페이스 선언을 꼭 같이 해주었던 것으로 생각됩니다.
