#what is ThreadLocal ?

스레드로컬이란 같은 스레드 내에서 공유되는 변수이다 (범위가 스레드인 로컬 변수)

ThreadLocal<UserInfo> local = new ThreadLocal<UserInfo>();

local.set(currentUser);

UserInfo userInfo = local.get();

이런 식으로 만들고, 넣고, 꺼내고 하면 될텐데 실제 사용하려면 static으로 ThreadLocal을 만들어야 할 것이다 (아니라면 파라미터로 계속 가지고 가야할꺼같다)

public class Content {
    public static ThreadLocal<Date> local = new ThreadLocal<Date>();
}


활용

한 스레드에서 실행되는 코드가 동일한 객체를 사용가능
사용자 인증정보 전파 - spring security 에서는 ThreadLocal로 전파하는 기능을 구현
트랜잭션 컨텍스트 전파 - 트랜잭션 매니저는 트랜잭션 컨텍스트를 전파
스레드에 안전해야 하는 데이터 보관
HistoryWriter , Log

주의점

스레드 풀 환경에서 사용시 데이터의 사용이 끝나면 반드시 지워줘야 한다


출처
https://m.blog.naver.com/PostView.nhn?blogId=agapeuni&logNo=220015077856&targetKeyword=&targetRecommendationCode=1
