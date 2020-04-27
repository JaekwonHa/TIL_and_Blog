# DO407 Automation with Ansible


* 일정
	* 장소 : 성수역 노브레이크 3층
	* 기간 : 2019.12.09 ~ 2019.12.12

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Contents**

- [Summary](#summary)
- [1장 Ansible 소개](#1%EC%9E%A5-ansible-%EC%86%8C%EA%B0%9C)
- [2장 Ansible 배포](#2%EC%9E%A5-ansible-%EB%B0%B0%ED%8F%AC)
  - [Inventory](#inventory)
  - [ansible.cfg](#ansiblecfg)
  - [애드혹 명령](#%EC%95%A0%EB%93%9C%ED%98%B9-%EB%AA%85%EB%A0%B9)
  - [2장 실습](#2%EC%9E%A5-%EC%8B%A4%EC%8A%B5)
- [3장 플레이북 구현](#3%EC%9E%A5-%ED%94%8C%EB%A0%88%EC%9D%B4%EB%B6%81-%EA%B5%AC%ED%98%84)
  - [playbook](#playbook)
  - [module 사용](#module-%EC%82%AC%EC%9A%A9)
  - [yaml 문자열](#yaml-%EB%AC%B8%EC%9E%90%EC%97%B4)
  - [3장 실습](#3%EC%9E%A5-%EC%8B%A4%EC%8A%B5)
- [4장 변수 및 팩트 관리](#4%EC%9E%A5-%EB%B3%80%EC%88%98-%EB%B0%8F-%ED%8C%A9%ED%8A%B8-%EA%B4%80%EB%A6%AC)
  - [변수](#%EB%B3%80%EC%88%98)
  - [시크릿 관리](#%EC%8B%9C%ED%81%AC%EB%A6%BF-%EA%B4%80%EB%A6%AC)
  - [팩트 관리](#%ED%8C%A9%ED%8A%B8-%EA%B4%80%EB%A6%AC)
  - [4장 실습](#4%EC%9E%A5-%EC%8B%A4%EC%8A%B5)
- [5장 작업 제어 구현](#5%EC%9E%A5-%EC%9E%91%EC%97%85-%EC%A0%9C%EC%96%B4-%EA%B5%AC%ED%98%84)
  - [반복분](#%EB%B0%98%EB%B3%B5%EB%B6%84)
  - [조건문](#%EC%A1%B0%EA%B1%B4%EB%AC%B8)
  - [핸들러](#%ED%95%B8%EB%93%A4%EB%9F%AC)
  - [작업 오류 제어](#%EC%9E%91%EC%97%85-%EC%98%A4%EB%A5%98-%EC%A0%9C%EC%96%B4)
  - [5장.실습](#5%EC%9E%A5%EC%8B%A4%EC%8A%B5)
- [6장 관리호스트에 파일 배포](#6%EC%9E%A5-%EA%B4%80%EB%A6%AC%ED%98%B8%EC%8A%A4%ED%8A%B8%EC%97%90-%ED%8C%8C%EC%9D%BC-%EB%B0%B0%ED%8F%AC)
  - [파일 관리](#%ED%8C%8C%EC%9D%BC-%EA%B4%80%EB%A6%AC)
  - [JINJA2 템플릿](#jinja2-%ED%85%9C%ED%94%8C%EB%A6%BF)
  - [6장 실습](#6%EC%9E%A5-%EC%8B%A4%EC%8A%B5)
- [7장 대형 프로젝트 관리](#7%EC%9E%A5-%EB%8C%80%ED%98%95-%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8-%EA%B4%80%EB%A6%AC)
  - [호스트 패턴으로 호스트 선택](#%ED%98%B8%EC%8A%A4%ED%8A%B8-%ED%8C%A8%ED%84%B4%EC%9C%BC%EB%A1%9C-%ED%98%B8%EC%8A%A4%ED%8A%B8-%EC%84%A0%ED%83%9D)
  - [동적 인벤토리 관리](#%EB%8F%99%EC%A0%81-%EC%9D%B8%EB%B2%A4%ED%86%A0%EB%A6%AC-%EA%B4%80%EB%A6%AC)
  - [병렬 구성](#%EB%B3%91%EB%A0%AC-%EA%B5%AC%EC%84%B1)
  - [파일 포함하기 및 가져오기](#%ED%8C%8C%EC%9D%BC-%ED%8F%AC%ED%95%A8%ED%95%98%EA%B8%B0-%EB%B0%8F-%EA%B0%80%EC%A0%B8%EC%98%A4%EA%B8%B0)
- [8장 역할로 플레이북 단순화](#8%EC%9E%A5-%EC%97%AD%ED%95%A0%EB%A1%9C-%ED%94%8C%EB%A0%88%EC%9D%B4%EB%B6%81-%EB%8B%A8%EC%88%9C%ED%99%94)
  - [Role](#role)
  - [Ansible-Galaxy](#ansible-galaxy)
  - [시스템 역할이 있는 콘텐츠 재사용](#%EC%8B%9C%EC%8A%A4%ED%85%9C-%EC%97%AD%ED%95%A0%EC%9D%B4-%EC%9E%88%EB%8A%94-%EC%BD%98%ED%85%90%EC%B8%A0-%EC%9E%AC%EC%82%AC%EC%9A%A9)
  - [8장 실습](#8%EC%9E%A5-%EC%8B%A4%EC%8A%B5)
- [9장 ANSIBLE 문제 해결](#9%EC%9E%A5-ansible-%EB%AC%B8%EC%A0%9C-%ED%95%B4%EA%B2%B0)
  - [플레이북 문제 해결](#%ED%94%8C%EB%A0%88%EC%9D%B4%EB%B6%81-%EB%AC%B8%EC%A0%9C-%ED%95%B4%EA%B2%B0)
  - [Ansible 관리 호스트 문제 해결](#ansible-%EA%B4%80%EB%A6%AC-%ED%98%B8%EC%8A%A4%ED%8A%B8-%EB%AC%B8%EC%A0%9C-%ED%95%B4%EA%B2%B0)
- [10장 LINUX 관리 작업 자동화](#10%EC%9E%A5-linux-%EA%B4%80%EB%A6%AC-%EC%9E%91%EC%97%85-%EC%9E%90%EB%8F%99%ED%99%94)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


## Summary
* 점식 식사에 당근이 들어간 반찬이 많이 나왔다 2당근 2당근 3당근 2당근
	* 잡채 ,불고기, 카레, 샐러드 등등..
* Ansible의 기초를 배울 수 있었던 교육
	* 변수 선언, 할당, 조건문, 반복문, 에러 핸들링, 외부 lib 사용, 복잡한 프로젝트 구성
* 기존에 스크립트나 일회성 command로 하던 것들을 **거의** 대부분 할 수 있다
	* ex. 특정 host, group에 대해서 방화벽이 모두 열려있는지 확인하고 싶다 -> 스크립트짜기 보다 ansible 애드혹 기능 사용하면 편함
	* 모든 서버에 ansible이 설치되야 활용도가 올라감
* 서버에서 수행되어야 하는 데몬, 서비스들을 service로 등록하면 관리포인트가 많이 줄어들고 자동화하기도 수월
	* 설치파일로 설치하는 것과 패키지 매니저를 이용한 설치의 차이점도 고민해볼만함
* 기본적인 linux 서버 환경 구성에 대한 이해 증가
* Ansible galaxy 활용
	* github 처럼 ansible role 들을 공유, 기여하는 커뮤니티, 툴
	* Ansible 에서 권장하는 role 단위의 프로젝트 구성을 도와줌
		* ansible role 스켈레톤 프로젝트 생성 명령어
			* 요즘은 이런건 기본인듯..
	* dependancy 명시하는 방식이나 프로젝트를 구성하는 방법이 프로그래밍 하는 것과 비슷
	* 우리가 활용해볼 포인트 ?
		* 우리는 서버를 프로비저닝 하는 단계는 개발자의 영역에서 하고 있지 않음
		* 서비스 빌드, 배포 하는 방식은 회사마다 다를 것이기에 굳이 여기에 맞춰야 하나 (프로비저닝 단계 역시 제각각)
		* redis나 ELK 구성하는 것들은 의존성 추가하고 사용하는게 편하지 않을까도 싶음
	* 믿고 쓸 수 있는가?
		* 서비스에서 외부 라이브러리를 사용하는 방식은..생각해보면 DEV,QA를 거치기에 검증이 됨
		* 외부 role을 사용한다는 것도 상당한 검증이 필요해보임
* Ansible 묻고 더블로
	* ansible 의 기본적인 모듈 활용 + 조건문 + 반복문 + 변수 활용 + ansible_facts (기본 변수) 를 얼마나 잘 쓰느냐
	* 복잡하게 구성하기 보다는 간단하게. 재사용 가능하게. 꾸준한 리팩토링
	* 타이핑이 상당히 많다. 오타나 줄바꿈, 대쉬 사용을 햇갈려 하지 않아야 한다
		* 영타 연습에 정말 좋았다. 맥북은 키보드 자체는 안좋다는걸 느낌

## 1장 Ansible 소개

* Ansible is simple
	* 사람이 읽을 수 있는 자동화를 제공
	* but 들여쓰기, ‘-‘ 를 잘 사용하는게 굉장히 중요하고 실수하기 쉽다
* Ansible is powerful
	* 물리머신, 클라우드, 네트워트 장비 모두 대응 가능
* Ansible si agentless
	* 설치할 필요가 없다
	* ssh 통신만 되면 managed host 제어 가능
* Ansible 아키텍쳐에서 등장하는 시스템
	* 제어노드 control node
		* 반드시 Linux / Unix 시스템
	* 관리 호스트 managed host
		* `WinRM`을 통해서 windows 시스템도 관리 가능
* task, role, play 멱등성
* Red hat Ansible Tower
	* 엔터프라이즈 프레임워크
	* 작성된 playbook을 관리하는 대시보드를 제공해주는 툴
	* 직접 playbook을 만드는 사람이 아닌 관리자들이 사용
* Ansible 사용 사례
	* config file 관리
	* build / deploy
	* provisioning
	* CI / CD
	* 보안 및 규정 준수

## 2장 Ansible 배포

### Inventory
* 관리할 호스트 컬렉션
* ansible.cfg 에 정의된 inventory 파일을 사용한다
	* default /etc/ansible/hosts
* 해당하는 hosts 출력 방법
	* ansible all -i inventory ——list-hosts
		* all, ungrouped 등과 같은 스페셜 host 있음
### ansible.cfg
* 우선 선위
	* /etc/ansible/ansible.cfg
	* ~/.ansible.cfg
	* ./ansible.cfg
	* ANSIBLE_CONFIG 환경변수 (가장 높음)
	* 사용자 수준 구성 파일에 정의하지 않은 설정은 디폴트 설정을 쓴다
* 섹션별로 설정을 정확하게 정의해줘야 한다
* 뭘 사용하게 될지 확인
	* `ansible —version`
* 보통 프로젝트에 아래처럼 입력

```yaml
[default]
inventory = ./inventory
```

* ansible.cfg 에 기술한 내용들을 play로 옮기게 됨
	* ansible.cfg 에 정의하면 전역으로 설정되는 느낌
* 연결 설정
	* managed host 에 control node 공개키를 배포해야함

```shell
ssh-keygen
ssh-copy-id user@…
or
authorized_key module 사용
```

* ssh 를 사용하지 않는 연결
	* ssh 연결 유형
		* ansible.cfg > [defaults] > transport = smart or local
	* local 연결 유형은 remote_user 설정을 무시하고 로컬 시스템에서 직접 실행한다
		* -u devops 로 remote_user 설정해도 무시됨
		* localhost 를 inventory 에 포함시킨다
			* all, ungrouped 그룹에 포함되므로 꺼려지는 방식
		* localhost 연결을 smart 로 변경
			* host_vars 하위에 localhost 파일 만들어서 `ansible_connection: smart`
* group_vars
	* 그룹 변수를 사용하여 호스트 그룹 전체에 변수 설정 가능

### 애드혹 명령
* 플레이북을 작성하지 않고 실행할 수 있는 단순한 온라인 작업
	* `ansible all -m ping`
* 관리호스트에서 임의의 명령 실행 방법
	* command, shell
		* 관리 호스트의 쉘에서 수행되지 않음
		* 쉘 환경 변수에 엑세스, 리디렉션, 파이프 등의 작업 불가
		* 관리 호스트에 python 필요
		* `ansible localhost -m command -a set`
		* `ansible localhost -m shell -a set`
	* raw
		* 원격 쉘에서 직접 명령 수행 가능
	* 위 방법들 모두 멱등을 보장하지 않기 때문에 사용하지 않는 것이 좋음

### 2장 실습
* `-o` 옵션으로 명령어 결과를 한줄로 표시가능
* .vimrc 추가

```shell
autocmd FileType yaml set local ts=2 sts=2 sw=2 expandtab
```

* 원격 장비에 대해서 ansible 로 명령 수행 가능

```shell
ansible servera.lab.example.com -m command -a 'systemctl status httpd'
```

## 3장 플레이북 구현

### playbook
* 대상 호스트 집합에 대해 여러개의 복잡한 작업을 수행

```yaml
- name:
	hosts:
	tasks:
```

* 작업이 나열되는 순서가 중요
* 모든 host 에 대해서 동시에 진행. 한대씩 진행이 필요하면 `serial: 1`

### module 사용
* module 이름을 모를 때
	* [Ansible Documentation — Ansible Documentation](https://docs.ansible.com/ansible/latest/index.html)
* module 이름을 알 때
	* `ansible-doc`
	* status 필드
		* stableinterface
		* preview
		* deprecated
		* removed

### yaml 문자열
* |
	
	* 문자열 내에 있는 개행 문자를 유지
* >
	
	* 개행 문자는 공백으로 변환

### 3장 실습
* firewalld module
	* permanent 연결이 영구적으로 적용되어 있는지 확인
	* immediate
* `ansible.cfg` 에 아래를 추가하면 결과를 human readable 하게 볼 수 있다
	* `stdout_callback= debug`

## 4장 변수 및 팩트 관리

### 변수
* Ansible 변수 범위
	* global
		* 명령줄 또는 Ansible 구성에서 설정한 변수
	* play
		* 플레이 및 관련 구조에서 설정한 변수
	* host
		* 인벤토리, 팩트 수집, 등록된 작업별로 호스트 그룹 및 개별 호스트에서 설정한 변수
* Playbook
	* 변수 정의 방법
		* Playbook 시작 위치에서 vars 블록에 변수를 배치
		* Playbook vars 블록 대신, vars_flies 지시어를 사용하여 파일에 정의된 변수를 배치
	* 변수 사용
		* 이중 중괄호 {{ }}
		* 첫번째 요소로 사용하는 경우에는 따옴표. “{{ }}"
* Host
	* 변수 정의 방법
		* 인벤토리 파일에 직접 정의
			* 추천 되는 방법은 아님
		* group_vars, host_vars 디렉토리 사용
			* 호스트, 그룹 명과 일치하는 파일을 찾아 변수를 포함시킨다

```yaml
# 인벤토리 파일에 직접 정의
[servers:vars]
user=joe
```

* 명령줄에서 변수 재정의
	* `asible-playbook main.yml -e “package=apache"`
* 등록된 변수
		* register 를 이용하여 명령 출력을 저장할 수 있다

```yaml
- name: Install
	hosts: all
	tasks:
    - name: Install
      yum:
		  name: httpd
        state: latest
      register: install_result
```

### 시크릿 관리
* Ansible vault
	* 자체 암호화 기능은 아니고 외부 python 도구 키트 사용
	* AES256 (구버전은 AES128)
* ansible-vault
	* create
	* view
	* edit
	* encrypt
	* decrpyt
	* rekey
* playbook 에서 사용
	* —vault-id
		* 상호 입력하려면 —vault-id @prompt / --ask-vault-pass
	* —vault-password-file
* 중요 변수만 암호화하는 것이 좋음
	* host_vars / group_vars 하위에 vars / vault 로 변수 관리 파일을 나누어 관리하는 것이 좋다
* vault 가속화
	* `sudo yum install python-cryptography`
	* playbook 에서 여러개의 vault 암호를 사용하는 경우 파일에 vault id 가 지정되었는지 확인하고 playbook 에서 해당 vault id 와 일치하는 암호를 입력해야 한다

### 팩트 관리
* 모든 play는 첫번째 작업 이전에 `setup` 모듈을 자동으로 실행한다
	* gather_fact: no 설정해도 수동으로 수집할 수 있다

```shell
ansible webserver -m setup
```

```yaml
tasks:
	- name: Manually gather facts:
	  setup
```

* 자주 쓰이는 ansible 팩트
	* 짧은 호스트 이름 : ansible_facts[‘hostname']
	* 정규화된 도메인 이름 : ansible_facts['fqdn']
	* 기본 IPv4 주소 : ansible_facts[‘default_ipv4']['address']
	* 모든 네트워크 인터페이스 이름 : ansible_facts['']
	* /dev/vda1 디스크 파티션 크기 : ansible_facts['devices']['vda']['partitions]['vda1']['size’]
	* DNS 서버목록 : ansible_facts[‘dns']['nameservers']
	* 현재 실행되고 있는 커널의 버전 : ansible_facts['kernel']
* 사용자 지정 팩트
	* ansible 에 등록될 팩트를 managed host 가 관리하게 할 수도 있다
	* 이러한 팩트는 setup 모듈에 의해 포준 팩트 목록으로 수집된다
		* `ansible_facts.ansible_local` 변수에 저장됨
	* `/etc/ansible/facts.d` 하위에 .fact 로 끝나는 파일이나 스크립트
		* INI, json 형식만 가능
* 매직 변수
	* setup 모듈에 의해서 구성되는게 아닌 ansible에 의해 자동으로 수집되는 변수
	* hostvars
		* 관리 호스트의 변수가 포함됨
		* 다른 관리 호스트의 변수를 가져올 수도 있다
		* hostvars[‘localhost’]
	* group_names
	* groups
	* inventory_hostname

### 4장 실습
* `htpasswd module`
	* 웹 사용자의 기본 인증에 사용할 htpasswd 파일을 생성하는 모듈
* .htaccess
	* 문서 디렉토리에 접근할 수 있는 권한이 정의된 파일

```shell
# -k 웹서버의 SSL 인증서 확인을 비활성화
curl https://serverb.lab.example.com -k -u guest
```


## 5장 작업 제어 구현

### 반복분
* 문법
	* loop
	* with_items
	* element는 {{ item }} 으로 접근 가능
* 반복문의 결과를 register 하게 되면
	* results 키에 작업 결과 list 가 저장된다

### 조건문
* 문법
	* when
		* when 에서는 {{ }} 사용하지 않음
	* is defined, is not defined, not variable (변수가 false), a in list
	* or, and
* 복수의 조건

```yaml
when: >
	( ansible_distribution == “RedHat" and
	  ansible_distribution_major_version == "7” )
	or
	( ansible_distribution == “Fedora" and
	  ansible_distribution_major_version == "28" )
```

### 핸들러
* 사용
	* 핸들러는 항상 handlers 섹션에 지정된 순서대로 동작
		* notify 순서와는 관계 없음
	* 다른 모든 작업이 완료된 후 수행됨
	* 핸들러 이름은 글로벌 네임 스페이스라 겹치게 되면 하나만 수행됨
	* 여러 곳에서 notify 해도 핸들러는 1번만 수행됨
	* notify 트리거는 작업 결과의 changed 상태 유무

### 작업 오류 제어
* 지시어
	* igrore_errors: yes
	* force_handlers: yes
	* failed_when: 
		* 작업을 수행한 후 보고하는 상태에 따라서 결정
	* changed_when: 
* block - rescue - always
	* try - catch - finally 의 ansible 버전

### 5장.실습
* `set_fact`
	* 변수에 값을 지정할 때 사용
	* register 가 task 결과물을 저장하는 용도라면 set_fact 는 임의의값을 저장 가능
* `shell, command`
	* 상태를 조회하는 것과 상태를 변경하는 것의 차이를 알지 못한다. 무조건 changed 상태가 떨어짐

## 6장 관리호스트에 파일 배포

### 파일 관리
* files module
	* blockinfile
	* copy
		* 로컬 또는 관리 호스트에서 관리 호스트로 파일을 복사
	* fetch
		* 관리 시스템에서 제어 노드로 파일을 복사
		* 파일 복사 위치 : `{dest}/{hostname}/{src}` 라서 의도와 다르게 동작할 수 있다
	* file
		* [file – Manage files and file properties — Ansible Documentation](https://docs.ansible.com/ansible/latest/modules/file_module.html)
		* state
			* touch
				* 파일이 존재하는지, 파일 소유자, 그룹 및 사용권한이 특정값이 맞는지 확인
				* 파일이 존재하면 수정 시간 업데이트, 존재하지 않으면 빈 파일 생성
			* absent
				* 파일 제거 (recursive)
			* directory
				* 폴더 생성 (recursive)
	* lineinfile
	* stat
	* syncronize
		* rsync 랩퍼
		* 용도에 따라서 run command rsync 로 직접 호출해줘야 할 수 있다
	* selinux 파일 컨텍스트
		* seuser, serole, setype, selevel

### JINJA2 템플릿
* 구분 기호
	* {% EXPR %}
	* {{ EXPR }}
	* {{ # COMMENT #}} 

### 6장 실습
* file 생성 후에 확인. 모든 host 에 대해서 한방에 확인 가능
	* `ansible all -m command -a ‘ls -Z' -u devops`
	
## 7장 대형 프로젝트 관리

### 호스트 패턴으로 호스트 선택
* *
	* 모든 인벤토리 이름, 호스트, 호스트 그룹과 일치한다
	* 그룹을 구분하지 않기 때문에 예상과 다르게 작동할 수 있다
* !
	* 차집합
	* `all,!datacenter1`
* &
	* AND
	* `lab,&datacenter1`
		* lab, datacenter1 두개 그룹에 모두 있는 호스트만

### 동적 인벤토리 관리
* 동적으로 인벤토리 정보를 JSON 형식으로 반환 해주는 스크립트를 사용할 수 있다
	* 모든 언어 사용 가능
* `ansible-inventory`
	* json 형식으로 인벤토리를 작성하는 방법을 습득할 때 도움이 됨
	* 인벤토리 파일의 콘텐츠를 JSON 형식으로 출력해줌
	* `ansible-inventory —list`
* 지원해야 하는 option
	* —list
		* 스크립트가 인벤토리와 모든 호스트와 그룹을 JSON 인코딩 해시/사전을 표준 출력으로 표시해야 함
	* —host manged_host
		* 해당 호스트와 연결해야하는 변수로 구성된 JSON 해시/사전을 표줄 출력으로 표시해야 함
* inventory_ignore_extensions
	* 특정 접미사로 끝나는 인벤토리 파일을 무시
* [Developing dynamic inventory — Ansible Documentation](https://docs.ansible.com/ansible/latest/dev_guide/developing_inventory.html)

```python
#!/usr/bin/env python

from subprocess import Popen,PIPE
import sys
import json

result = {}
result[‘webservers’] = {}
result[‘webservers’][‘hosts’] = []
result[‘webservers’][‘vars’] = {}

pipe = Popen([‘getent’, ‘hosts’], stdout=PIPE, universal_newlines=True)

for line in pipe.stdout.readlines():
   s = line.split()
   if s[1].startswith(‘servera'):
      result['webservers’][‘hosts’].append(s[1])

if len(sys.argv) == 2 and sys.argv[1] == ‘—list’:
    print(json.dumps(result))
elif len(sys.argv) == 3 and sys.argv[1] == ‘—host’:
    print(json.dumps({}))
else:
    print(“Requires an argument, please use —list or —host <host>")
```

### 병렬 구성
* forks
	* 작업 당 최대 연결 개수 (module)
* serial
	* play 당 최대 연결 개수

### 파일 포함하기 및 가져오기
* import_tasks, import_roles, import_playbook
	* 작업 파일을 가져올 때 플레이북 구문 분석 시 직접 삽입됨
	* **변수를 사용하여 파일 이름을 지정할 때는 호스트 또는 그룹 인벤토리의 변수를 사용할 수 없음**
	* **when 조건문이 가져온 모든 작업에 적용된다**
* include_tasks, include_roles
	* 동적으로 삽입됨
	* notify 로 포함된 작업 파일에 있는 핸들러 이름을 호출 할 수 없다
	* **when 조건문이 작업 파일을 가져올지 말지 결정한다**
* [Conditionals — Ansible Documentation](https://docs.ansible.com/ansible/latest/user_guide/playbooks_conditionals.html#applying-when-to-roles-imports-and-includes)
* 실습
	* 	정적 인벤토리 파일에서는 참조하는 모든 호스트 그룹이 정의 되어 있어야 한다

## 8장 역할로 플레이북 단순화

### Role
* 역할 = role
	* 컨텐츠를 그룹화하고 다른 사용자와 쉽게 공유하고 재사용이 용이하다
	* 목적에 따라서 역할을 정의할 수 있다
	* 큰 프로젝트를 관리하기 쉽게 해준다
* ansible 역할 구조
	* ansible-galaxy init
		* defualts
			* 재정의 하지 않을 변수들
		* files
		* handlers
		* meta
			* 작성자, 라이센스, role dependency 정보
		* tasks
		* templates
		* tests
		* vars
	* 변수 적용 우선순위
		* 글로벌
		* role call 변수
		* vars
		* playbook
		* inventory
		* defualt
* 실행 순서 제어
	* pre_tasks, post_tasks 를 통해서 role 수행 전/후로 추가 수행할 task 를 지정가능
* 역할 내용 개발을 위한 권장 사례
	* ansible-galaxy init 후에 필요없는 디렉터리, 파일 삭제
	* README.md, meta/main.yml 을 유지, 관리하고 사용법을 문서 한다
	* 역할은 특정 목적이나 기능에 집중한다
	* 역할은 자주 재사용하고 리팩토링 한다

### Ansible-Galaxy
* [Ansible Galaxy](https://galaxy.ansible.com/)
	* 공용 Ansible Role 라이브러리
	* 각각의 기능을 하는 여러가지 Role 들이 제공되고 기여할 수 있다
	* ansible-galaxy cli
		* ansible-galaxy search
			* —author
			* —playform
			* —galaxy-tags
		* ansible-galaxy info
		* ansible-galaxy install
			* 	-r roles/requirements.yml
				* 특정 역할에 의존성이 있는 경우 requirements.yml 에 기록해야 하고 의존성 role 들을 위의 옵션으로 설치할 수 있다
		* ansible-galaxy init
		* ansible-galaxy list
			* ansible.cfg 파일에 있는 roles_path 항목에 있는대로 아래 3개 항목에 대해서 role을 검색한다
				* ./roles
				* /usr/share/ansible/roles
				* /etc/ansible/roles
		* ansible-galaxy remove

```yaml
# requirements.yml
- src: https://gitlab.com/guardianproject-opt/ansible-nginx-acme.git
scm: git
version: master
name: nginx-acme
```

### 시스템 역할이 있는 콘텐츠 재사용
* RED HAT ENTERPRISE LINUX 시스템 역할
	* RHEL 7.4 부터 다수의 ansible role이 Extras 채널에서 rhel-system-roles 패키지의 일부로 운영체제에서 제공되기 시작
	* rhel-system-roles.kdump
	* rhel-system-roles.network
	* rhel-system-roles.selinux
	* rhel-system-roles.timesync
	* rhel-system-roles.postfix
	* rhel-sytsem-roles.firewall
	* reel-system-roles.tuned
	* 사용 방법

```shell
# Extras 채널을 활성화
subscription-manager repos --enable rhel-system-extras-rpme 
# RHEL system role 설치
yum install rhel-system-roles
# 설치 확인
ls -l /usr/share/ansible/roles
```

### 8장 실습
* password: “{{ ‘redhat’ | password_hash('sha512’, 'mysecretsalt' ) }}'
* prompt 에 표시되는 [user@hostname ~] 변경 방법
	* .bashrc PS1=[\u on \h in \W dir]$
		* 유저, 호스트네임, 현재경로

## 9장 ANSIBLE 문제 해결

### 플레이북 문제 해결
* 로그 저장
	* ansible.cfg 내에 log_path = ansible.log
* debug module
	* msg
		* 메시지를 출력
	* var
		* 변수를 출력
	* verbosity
		* -v -vv -vvv -vvvv
* 오류 관리
	* --step
		* 하나씩 수행
		* --start-at-task
		* 선택한 작업부터 시작

### Ansible 관리 호스트 문제 해결
* --check
	* playbook 에서 스모크 테스트를 수행
	* 변경된 사항이 표시되지만 실제 수행되지는 않는다
	* 모듈에서 지원되지 않으면 변경 사항을 표시되지 않지만 수행되지 않는다
	* check_mode: yes
		* --check 여부와 상관없이 항상 check mode 로 수행됨
	* check_mode: no
		* —check 여부와 상관없이 항상 수행됨
		* 이전 버전의 always_run: yes 를 대체함
		* check mode 사용시 주의해야함
* 테스트할 모듈
	* fail module
	* script modile
		* 스크립트 return code 0 이 아니면 실패
	* assert module
* 연결 문제 해결
	* ansible 대부분의 문제가 호스트 연결 및 원격 사용자와 권한 에스컬레이션의 문제다
	* ansible_host 변수를 설정함으로써 연결할 호스트를 설정할 수 있다
		* inventory file
			* web4.phx.example.com ansible_host=192.0.2.4
* 올바른 테스트 수준
	* [Testing Strategies — Ansible Documentation](https://docs.ansible.com/ansible/latest/reference_appendices/test_strategies.html)

## 10장 LINUX 관리 작업 자동화

* 일반적인 로컬 사용자 관리 메뉴얼
	* 모든 호스트가 동일한 로컬 사용자를 사용할 수 있어야 합니다.
	* 이러한 사용자는 암호를 지정하지 않고 sudo 명령을 사용할 수 있는 webadmin 사용자 그룹에 속해야 합니다.
	* 또한 사용자의 SSH 공개 키는 환경에 배포되어야 하며 root 사용자는 직접 SSH를 사용하여 로그인할 수 없어야 합니다.
	* users, groups module 사용자 및 그룹이 관리 대상 노드에 있는지 확인하고 일관성 유지
	* authroized_key module SSH 키 인증이 다양한 사용자들에 대해 구성되어 있는지 확인
	* lineinfile module 
		* /etc/sudoers 파일을 수졍하여 암호없이 sudo 명령을 사용할 수 있도록 허용한다
		* /etc/ssh/sshd_config 파일을 수정하여 root 사용자로 SSH 접속을 허용하지 않는다
			* `PermitRootLogin no`
			* restart sshd
* cron module
	* cron 설정
	* cron 위치
		* /var/spool/cron
		* /etc/cron.d
			* 이 위치에 각각의 crontab name 으로 파일을 생성
		* /etc/crontab 
* 스토리지 관리
	* 웹 서버 구성에 권장되는 방법은 웹 서버 데이터를 별도의 파티션이나 논리 볼륨에 저장하는 것
		* log, content file 등
	* `lsblk`
		* 물리볼륨, 논리볼륨 조회 명령어 
	* 파티션 -> 볼륨 그룹 -> 논리 볼륨 생성
		* parted, lvg, lvol
	* 논리 볼륨의 용량을 줄이는 경우 (수정 후 ansible 수행) XFS 파일 시스템이 용량 축소를 지원하지 않으므로 아래의 작업은 실패

```yaml
- name: Ensure the correct capacity for each LV
	lovl:
		vg: “{{ item.vgroup }}”
		lv: “{{ item.name }}”
		size: “{{ item.size }}”
		resizes: yes
		force: yes
	loop: “{{ logical_volumes }}”
```

