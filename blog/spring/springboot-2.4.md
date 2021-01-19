# Spring Boot 2.4 변경 내용
> https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-2.4-Release-Notes
> https://spring.io/blog/2020/11/12/spring-boot-2-4-0-available-now

## 주관적인 주요 변경 사항

* JUnit 5’s Vintage Engine Removed from spring-boot-starter-test
* Config File Processing (application properties and YAML files)
* Embedded database detection
* Custom property name support
* Volume Mounted Config Directory Trees

## Versioning scheme change

2.4 버전부터는 새로운 Spring 버저닝 전략을 사용합니다. build.gradle/pom.xml에 spring boot 버전을 명시할때 뒤에 .RELEASE 와 같은 부분을 더 이상 작성하지 않습니다.

```shell
#as-is
2.4.0.RELEASE
#to-be
2.4.0
```

## JUnit 5’s Vintage Engine Removed from spring-boot-starter-test

Vintage Engine이 `spring-boot-stater-test`에서 제거되었습니다.

Vintage Engine은 Junit4로 작성된 테스트들도 JUnit5 환경에서 실행될 수 있도록 해주었습니다.

만약 JUnit4 지원이 필요하다면 아래와 같은 의존성 추가가 필요합니다.

```xml
<dependency>
    <groupId>org.junit.vintage</groupId>
    <artifactId>junit-vintage-engine</artifactId>
    <scope>test</scope>
    <exclusions>
        <exclusion>
            <groupId>org.hamcrest</groupId>
            <artifactId>hamcrest-core</artifactId>
        </exclusion>
    </exclusions>
</dependency>
```
```yaml
testImplementation("org.junit.vintage:junit-vintage-engine") {
    exclude group: "org.hamcrest", module: "hamcrest-core"
}
```

## Config File Processing (application properties and YAML files)

`application.properties` / `application.yml` 파일을 간단하게 사용 중이라면 2.4 전환이 문제없이 될 것입니다.

하지만 profile 별로 properties를 다르게 설정한다던가, 좀 더 복잡한 설정을 사용한다면 변경 사항들이 있습니다.

> 참고: [Spring Boot Config Data Migration Guide](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-Config-Data-Migration-Guide)

### Legacy Mode

새로운 config data 처리 방식을 적용하고 싶지 않다면, 아래 설정을 추가합니다.

```yaml
spring.config.use-legacy-processing=true
```

### Multi-document YAML Ordering

`---`로 profile 구분이된 multi document YAML 파일을 사용 중이라면 profile 활성화 순서에 변화가 있습니다.

2.4 이전버전에서는 profile이 선언된 순서에 따라 document가 추가되었지만, 2.4 버전부터는 상단에 선언된 document가 먼저 추가됩니다.

덮어쓰는 속성이 있다면 나중에 추가되는 document가 속성을 덮어쓰게 됩니다.

### Profile Specific External Configuration

2.4 이전버전에서는 jar 파일 외부의 application.properties 파일이 jar 파일 내부의 application-<profile>.properties 파일을 덮어쓰지 않았습니다.

2.4 버전부터는 특정 profile에 대한 파일이든 아니든, 외부 파일이 jar 내부 파일을 항상 덮어쓰게 됩니다.

### Profile Specific Documents

`spring.profiles` 속성을 사용하고 있다면 `spring.config.activate.on-profile` 속성으로 변경해야 합니다.

### Profile Activation

2.4 버전부터는 특정 profile document에는 spring.profiles.active, spring.profiles.include 를 사용할 수 없습니다.

> 특정 profile document란 yaml 파일 내부에 `---`로 구분된 각 profile 영역

spring.profiles.include는 spring.profiles.group."profile" 속성으로 변경되었습니다.

```yaml
# as-is
spring.application.name: "customers"
---
spring.profiles: "production"
spring.profiles.include: "mysql,rabbitmq"
---
spring:
  profiles: "mysql"
  datasource:
    url: "jdbc:mysql://localhost/test"
    username: "dbuser"
    password: "dbpass"
---
spring:
  profiles: "rabbitmq"
  rabbitmq:
    host: "localhost"
    port: 5672
    username: "admin"
    password: "secret"

# to-be
spring:
  application:
    name: "customers"
  profiles:
    group:
      "production": "mysql,rabbitmq"
---
spring:
  config:
    activate:
      on-profile: "mysql"
  datasource:
    url: "jdbc:mysql://localhost/test"
    username: "dbuser"
    password: "dbpass"
---
spring:
config:
  activate:
    on-profile: "rabbitmq"
  rabbitmq:
    host: "localhost"
    port: 5672
    username: "admin"
    password: "secret"
```

추가적으로 production instance에는 application-prod.yaml 파일이 있습니다.

`spring.profiles.active=prod` 속성을 설정하거나, `SPRING_PROFILES_ACTIVE=prod` 속성을 설정하면 application-prod.yaml 파일을 가져올 것 입니다.

이때 2.4 버전부터는 모든 외부 파일이 내부 파일을 override 하기 때문에 application-prod.yaml 파일을 application.yaml 로 이름변경하는 것도 가능합니다.

## Config Data Imports

`spring.config.import`, `spring.config.import` 속성 사용시에 파일이 실제로 없을때 실패시키지 않게 하기 위해서 `optional:` prefix를 사용할 수 있습니다.

```yaml
spring.config.location=optional:/etc/config/application.properties
```

모든 위치에 대해서 optional 설정을 주고 싶다면 `spring.config.on-not-found=ignore` 속성을 주거나 `SpringApplication.setDefaultProperties(...)`를 사용하거나 환경 변수 설정을 해줍니다.

## Embedded database detection 

H2, HSQL, Derby 등의 embedded database 사용 시에 in-memory 모드로 실행해야만 embedded database로 인식하고 동작합니다.

이로 인해 server 모드로 실행시에 아래와 같은 변경 사항이 발생합니다.

* `sa` username이 기본으로 설정되지 않습니다. `spring.datasource.username=sa` 속성을 따로 선언해주어야 합니다.
* DB 초기화가 자동으로 수행되지 않습니다. `spring.datasource.initialzation-mode` 속성을 따로 선언해주어야 합니다.

## Logback Configuration Properties

다음과 같이 속성값, 환경변수 이름이 변경되었고, 이전에 쓰던 이름은 deprecated 되었습니다.

```yaml
# properties
logging.pattern.rolling-file-name → logging.logback.rollingpolicy.file-name-pattern

logging.file.clean-history-on-start → logging.logback.rollingpolicy.clean-history-on-start

logging.file.max-size → logging.logback.rollingpolicy.max-file-size

logging.file.total-size-cap → logging.logback.rollingpolicy.total-size-cap

logging.file.max-history → logging.logback.rollingpolicy.max-history

# 환경 변수
ROLLING_FILE_NAME_PATTERN → LOGBACK_ROLLINGPOLICY_FILE_NAME_PATTERN

LOG_FILE_CLEAN_HISTORY_ON_START → LOGBACK_ROLLINGPOLICY_CLEAN_HISTORY_ON_START

LOG_FILE_MAX_SIZE → LOGBACK_ROLLINGPOLICY_MAX_FILE_SIZE

LOG_FILE_TOTAL_SIZE_CAP → LOGBACK_ROLLINGPOLICY_TOTAL_SIZE_CAP

LOG_FILE_MAX_HISTORY → LOGBACK_ROLLINGPOLICY_MAX_HISTORY
```

## Default Servlet Registration

2.4 이전버전에서는 static resource(html, js, css, image)등을 처리하기 위한 `DefaultServlet`(path: /)이 자동으로 등록되었습니다.

SpringBoot에서는 사실상 `DispatcherServlet`만 사용하기 떄문에 기본적으로 등록되던 `DefaultServlet`이 더 이상 등록되지 않습니다.

필요하다면 `server.servlet.register-default-servlet=true`로 사용할 수 있습니다.

## HTTP traces no longer include cookie headers by default

요청 헤더와 응답 헤더의 `Cookie`, `Set-Cookie`가 더 이상 자동으로 Actuator HTTP trace 응답에 포함되지 않습니다.

필요하다면 `management.trace.http.include=cookies, errors, request-headers, response-header`로 사용할 수 있습니다.

## Undertow Path on Forward

Undertow 환경에서 요청이 forward 될때 request URL이 유지되지 않습니다. 이는 Servlet spec을 준수하기 위해 변경되었습니다.

필요하다면 `server.undertow.preserve-path-on-forward=true`로 사용할 수 있습니다.

## Neo4j

Neo4j에 대한 지원이 상당부분 변경되었습니다. 많은 `spring.data.neo4j.*` 속성이 제거되었고, Neo4j OGM 지원도 중단되었습니다.

Neo4j driver 설정은 spring.neo4j.* 네임스페이스를 통해 가능하며, 자세한 사항은 이곳을 [참고](https://docs.spring.io/spring-data/neo4j/docs/6.0.x/reference/html/) 부탁드립니다.

## Hazelcast 4

SpringBoot 2.4버전은 Hazelcast 3.2.x와 호환성을 유지하면서 Hazlecast 4로 업그레이드합니다.

Hazelcast 3.2.x 유지가 필요하다면 hazelcast.version 속성을 사용하여 다운그레이드 할 수 있습니다.

## Elasticsearch RestClient

더 이상 하위 수준의 Elasticsearch `RestClient` bean이 자동으로 auto-configure 되지 않습니다.

`RestHighLevelClient`는 auto-configure 유지됩니다.

사용자들은 하위 수준 client가 직접적으로 필요한 경우는 거의 없으므로 이 변경사항에 영향을 받지 않아야 합니다.

## R2DBC

R2DBC의 핵심 인프라가 새로운 `spring-r2dbc` 모듈로 이동했습니다.

기존에 R2DBC의 핵심 인프라를 사용 중이였다면 deprecate 된 기능을 새로운 인프라로 전환해야합니다.

## Flyway

Flyway 7으로의 업그레이드는 [Callback Ordering](https://github.com/flyway/flyway/issues/2785)과 관련된 중요한 변경사항을 포함합니다.

기존에 다수의 callback이 존재할때 java callback이냐 SQL callback이냐에 따라서 적용되는 ordering 로직이 달랐습니다.

Flyway 7에서는 이름 기준의 Global Ordering이 적용됩니다.

Flyway 5를 사용 중이였다면, SpringBoot 2.4로 업그레이드 하기 전에 Flyway 6로 먼저 업그레이드 해야합니다.

## Removal of Plugin Management for Flatten Maven Plugin

SpringBoot는 더 이상 Flatten Maven Plugin을 사용하지 않고, 관련된 plugin management들이 제거되었습니다.

## Version management for exec-maven-plugin

`exec-maven-plugin`의 version management가 제거되었습니다. 해당 plugin을 사용한다면 pluginManagement에 버전을 명시해야 합니다.

## Spring Boot Gradle Plugin

SpringBoot Gradle Plugin DSL이 업데이트되어 mainClassName 대신 mainClass를 사용해야 합니다.

```groovy
// as-is
bootJar {
    mainClassName 'com.example.ExampleApplication'
}
// to-be
bootJar {
    mainClass 'com.example.ExampleApplication'
}
```

> 2.4 ReleaseNote에는 위와 같이 변경해야 한다고 나오고, [SpringBoot Gradle Plugin BootJar Task](https://docs.spring.io/spring-boot/docs/current/gradle-plugin/api/org/springframework/boot/gradle/tasks/bundling/BootJar.html#getMainClass--))를 보면 mainClassName 관련된 것들이 deprecated 된 것을 확인할 수 있습니다.
> 
> 다만 Intellij(2020.3)에서 프로젝트를 만들고 mainClass 설정을 해주면 Type 불일치로 실패하고 있으니, 원인을 찾기 전에는 mainClassName을 쓰도록 하는게 맞아보입니다.

## Metrics export in integration tests

@SpringBootTest 어노테이션을 사용하여 SpringBoot Integration Test 진행 시에 모니터링 시스템이 자동 제공되지 않고, in-memory `MeterRegistry` 정도만 제공됩니다.

Metric 정보가 필요하다면 `@AutoConfigureMetrics`를 사용해야 합니다.

## Deprecations from Spring Boot 2.2 and 2.3

SpringBoot 호환성 정책에 따라서 2.2에서 deprecated 된 것들이 2.4에서 제거되었습니다.

2.3에서 deprecated 된 것들은 2.5에서 제거 될 예정입니다.

## New and Noteworthy

configuration 전체 변경 사항들을 [참고](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-2.4.0-Configuration-Changelog) 부탁드립니다.

## Spring Framework 5.3

SpringBoot 2.4는 Spring Framework 5.3을 사용합니다. 전체 변경 사항을 [참고](https://github.com/spring-projects/spring-framework/wiki/What%27s-New-in-Spring-Framework-5.x) 부탁드립니다.

## Spring Data 2020.0

SpringBoot 2.4는 Spring Data 2020.0을 사용합니다. 전체 변경 사항을 [참고](https://github.com/spring-projects/spring-data-commons/wiki/Release-Train-Ockham-%282020.0.0%29) 부탁드립니다.

## Neo4j

해당 Release는 reactive repository에 대한 지원과 Neo4j driver에 대한 별도의 auto-configuration을 지원합니다. 따라서 더이상 Spring Data 없이도 Neo4j를 사용할 수 있습니다.

Neo4j에 대한 Health Check는 Driver를 사용하며 Neo4j driver가 configure되어 있으면 동작합니다.

`@Transactional`을 reactive access에 사용한다면 다음과 같은 `Neo4jReactiveTransactionManager` 설정이 필요합니다.

```java
@Bean(ReactiveNeo4jRepositoryConfigurationExtension.DEFAULT_TRANSACTION_MANAGER_BEAN_NAME)
public ReactiveTransactionManager reactiveTransactionManager(Driver driver,
      ReactiveDatabaseSelectionProvider databaseNameProvider) {
    return new ReactiveNeo4jTransactionManager(driver, databaseNameProvider);
}
```

## R2DBC

entity를 통한 Reactive R2DBC 사용을 단순화하기 위해서 `R2dbcEntityTemplate`을 사용할 수 있습니다.

## Java 15 Support

Java 15를 완벽하게 지원하고, 최소 지원 버전은 Java 8 입니다.

## Custom property name support

Properties 클래스를 선언할 때 Immutable 객체로 만들어주기 위해 `@ConstructorBinding`을 사용합니다.

이때 property 이름은 생성자의 parameter 이름을 따라가는데, java 예약어의 경우 parameter 이름으로 써줄 수 없는 문제가 있습니다.

이를 해결하기 위해 @Name 어노테이션을 사용할 수 있고, 아래 예제는 `sample.import` 라는 property로 사용가능합니다.

```java
@ConfigurationProperties(prefix = "sample")
@ConstructorBinding
public class SampleConfigurationProperties {

  private final String importValue;

  public SampleConfigurationProperties(@Name("import") String importValue) {
    this.importValue = importValue;
  }
}
```

## Layered jar enabled by default

Layered jar 형태를 활성화와 layertool 포함이 default로 제공됩니다. 이는 docker image 생성 시 효율이 향상됩니다.

자세한 사항은 [참고](https://docs.spring.io/spring-boot/docs/2.4.0/reference/html/spring-boot-features.html#layering-docker-images) 부탁드립니다.

## Importing Additional Application Config

`spring.config.use-legacy-processing=true` 설정을 사용하는게 아니라면, 추가적인 properties, yaml 파일을 직접 추가할 수 있습니다.

`spring.config.import` property를 사용하여 한개 혹은 여러개의 config 파일을 추가할 수 있고, [가이드](https://docs.spring.io/spring-boot/docs/2.4.0/reference/html/spring-boot-features.html#boot-features-external-config-files-importing)를 참고 부탁드립니다.

## Volume Mounted Config Directory Trees

`spring.config.import` property는 configuration tree를 import하는 방식으로도 사용할 수 있고, 이런 방식은 kubernetes 환경에서 매우 유용합니다.

예를 들어 kubernetes에서 아래와 같은 volume을 마운트했다고 해봅시다.

```
etc/
  config/
    myapp/
      username
      password
```

username은 config value이고, password는 secret일 수 있습니다. 이런 구조를 import 하기 위해서 아래와 같이 설정할 수 있습니다.

```properties
spring.config.import=optional:configtree:/etc/config/
```

myapp.username, myapp.password 와 같이 property에 접근이 가능합니다.

## Importing Config Files That Have no File Extension

몇몇 Cloud platform은 file 확장자가 없는 volume mount file만 제공할 수 있는 경우가 있습니다.

이런 제약사항이 있다면 다음과 같이 힌트를 줌으로써 file 확장자가 없는 파일을 특정 확장자를 가진 것처럼 로드할 수 있습니다.

```properties
spring.config.import=/etc/myconfig[.yaml]
```

## Origin Chains

`Origin` interface에 `getParent()` 메소드가 추가됩니다.

예를 들어 `spring.config.import`로 두번째 config 파일을 import 할 수 있습니다.

이때 두번째 파일에서 로드된 properties의 `Origin`에서 parent를 알 수 있습니다.

`actuator/env`, `actuator/configprops` actuator endpoint에서 확인할 수 있습니다.

## Startup Endpoint

actuator endpoint로 `startup`이 추가되었습니다. 이는 실행시간이 오래 걸리는 bean들을 확인하는데 도움을 줍니다.

## Docker/Buildpack Support

### Publishing Images

Maven plugin `spring-boot:build-image` goal과 gradle plugin `bootBuildImage` task가 생성된 image를 docker registry에 업로드하는게 가능합니다.

[Maven](https://docs.spring.io/spring-boot/docs/2.4.0/maven-plugin/reference/htmlsingle/#build-image-example-publish), [Gradle](https://docs.spring.io/spring-boot/docs/2.4.0/gradle-plugin/reference/htmlsingle/#build-image-example-publish)를 참고 부탁드립니다.

### Authentication

Spring Boot의 buildpack support를 사용해서 builder나 image 실행 시에 private docker registry를 사용할 수 있습니다.

username/password 방식과 token 기반 인증도 지원합니다.

[Maven](https://docs.spring.io/spring-boot/docs/2.4.0/maven-plugin/reference/htmlsingle/#build-image-docker-registry), [Gradle](https://docs.spring.io/spring-boot/docs/2.4.0/maven-plugin/reference/htmlsingle/#build-image-docker-registry)를 참고 부탁드립니다.

### Paketo Buildpack Defaults

Maven plugin `spring-boot:build-image` goal과 gradle plugin `bootBuildImage` task가 최신 Paketo images를 default로 사용합니다.

Paketo image registry는 접근성 향상을 위해 GCR에서 Docker hub로 변경되었습니다.

## Maven Buildpack Support

`spring-boot:build-image` Maven goal을 사용하면 모든 project module 의존성을 "application" layer에 담게됩니다.

multiple project module로 구성했다면 모두 같은 layer에 담기게 된다는 것을 의미합니다.

커스텀하기 위해서 `<includeModuleDependencies/>`, `<excludeModuleDependencies/>`를 사용할 수 있습니다.

## Gradle Buildpack Support

`bootBuildImage` Gradle task를 사용하면 모든 project module 의존성을 "application" layer에 담게됩니다.

multiple project module로 구성했다면 모두 같은 layer에 담기게 된다는 것을 의미합니다.

커스텀하기 위해서 `includeProjectDependencies()`, `excludeProjectDependencies()`를 사용할 수 있습니다.

## Redis Cache Metrics

Micrometer를 통해서 Redis cache 통계를 노출할 수 있습니다. put, get, delete, hits/misses 항목을 포함합니다. 대기 중인 요청 수와 잠금 대기 기간도 기록됩니다.

`spring.cache.redis.enable-statistics=true`로 활성화할 수 있습니다.

## Web Configuration Properties

Spring MVC와 Spring WebFlux 모두를 지원하는 새로운 Property들이 추가되었습니다.

* spring.web.locale
* spring.web.locale-resolver
* spring.web.resources.*
* management.server.base-path

기존에 Spring MVC를 위해 사용하던 아래 Property들은 deprecated 되었습니다.

* spring.mvc.locale
* spring.mvc.locale-resolver
* spring.resources.*
* management.server.servlet.context-path

## Register @WebListeners in a way that allows them to register servlets and filters

Servlet @WebListener 클래스는 자체적으로 서블릿, 필터를 등록 할 수 있는 방법을 제공합니다.

기존에는 `javax.servlet.Registration.Dynamic`를 사용하여 서블릿, 필터를 등록하였습니다.

2.4 버전부터는 dynamic registration을 사용하지 않고, `ServletContextListener.contextInitialized` 메소드 내부에서 `event.getServletContext().addServlet(…)`, `event.getServletContext.addFilter(…)`을 호출해야 합니다.

## Slice Test for Cassandra

Cassandra를 사용할 떄 `@DataCassandraTest` 어노테이션을 사용해서 Slice Test를 진행할 수 있습니다. Cassandra와 관련된 필수적인 인프라만이 구성됩니다.

아래는 `@DynamicPropertSource`를 사용하여 구성한 예입니다.

```java
@DataCassandraTest(properties = "spring.data.cassandra.local-datacenter=datacenter1")
@Testcontainers(disabledWithoutDocker = true)
class SampleDataCassandraTestIntegrationTests {

	@Container
	static final CassandraContainer<?> cassandra = new CassandraContainer<>().withStartupAttempts(5)
			.withStartupTimeout(Duration.ofMinutes(2));

	@DynamicPropertySource
	static void cassandraProperties(DynamicPropertyRegistry registry) {
		registry.add("spring.data.cassandra.contact-points",
				() -> cassandra.getHost() + ":" + cassandra.getFirstMappedPort());
	}
	...

}
```

## Flyway 7

spring.flyway 하위에 새로운 property가 추가되었습니다.

* open source edition
  * url
  * user
  * password
* teams edition
  * cherry-pick
  * jdbc-properties
  * oracle-kerberos-cache-file
  * oracle-kerberos-config-file
  * skip-executing-migrations

## Configuration property for H2 Console’s web admin password

H2 Console의 web admin 비밀번호를 `spring.h2.console.settings.web-admin-password`를 통해 설정할 수 있습니다.

console의 preferences, tools에 대한 접근을 제어합니다.

## CqlSession-Based Health Indicators for Apache Cassandra

새로운 `CqlSession`를 기반으로 한 `CassandraDriverHealthIndicator`, `CassandraDriverReactiveHealthIndicator`이 추가되었습니다. classpath에 Cassandra Java Driver가 있을때 auto-configure됩니다.

기존의 Spring Data Cassandra 기반의 health indicator는 deprecated 되었습니다.

## Filtered Scraping with Prometheus

Actuator의 Prometheus endpoint인 `/actuator/prometheus`에서 `includedNames` query parameter를 지원합니다.

## Spring Security SAML Configuration Properties

SAML2 relying party registration의 decryption credential, Assertion Consumer Service(ACS) 관련된 property들이 추가되었습니다. 

* spring.security.saml2.relyingparty.registration.decryption.*
* spring.security.saml2.relyingparty.registration.acs.*

## Failure Analyzers

`ApplicationContext`가 생성되지 않은 경우에도 FailureAnalizers가 고려됩니다. 이를 통해 환경 처리 중에 발생한 모든 예외를 분석 할 수도 있습니다.

`BeanFactoryAware` 또는 `EnvironmentAware`를 구현하는 분석기는 `ApplicationContext`가 생성되지 않는 한 사용되지 않습니다.

## Jar Optimizations

실행가능한 SpringBoot jar 파일을 만들때, 비어있는 starter dependencies는 자동적으로 제거됩니다.

starter는 의존성 정보만 제공하기에 최종적인 jar 파일에 패키징될 필요가 없습니다.

build 중에만 필요한 SpringBoot annotaion processor도 제거됩니다. `spring-boot-autoconfigure-processor`, `spring-boot-configuration-processor`이 있습니다.

code 없는 자체적인 starter POM이 있는 경우 "dependencies-starter" 값을 사용하여 Spring-Boot-Jar-Type 항목을 MANIFEST.MF에 추가할 수 있습니다.
