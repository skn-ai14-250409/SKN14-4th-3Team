# SKN14-4th-3Team
Repository for SKN14-4th-3Team

# 삼성전자/LG전자 세탁기·건조기 매뉴얼 Q&A 챗봇 “워시톡”(WashTalk)

---

🗓️ **진행 기간**: 2025년 8월 7일 ~ 8월 8일

---

##  팀 소개 


 유용환, 윤이서, 김준기, 이수미, 김재우, 정유진 

### **담당 업무**
| 이름   | 역할                                    |
|--------|---------------------------------------|
| 유용환 | HTML, CSS, Javascript 활용 프론트 웹페이지 구현, PINECONE VectorDB 구축, 연동    |
| 윤이서 | HTML, CSS, Javascript 활용 프론트 웹페이지 구현, 제품 url 소스 링크 제공 (매뉴얼 다운로드/크롤링), Figma 화면 설계  |
|        | AWS 클라우드에 인프라 구성, 프로젝트 문서 기록, 통합 테스트 진행 및 결과 보고서 작성     |
| 김준기 | HTML, CSS, Javascript 활용 프론트 웹페이지 구현, django 파일 작성 및 Docker 작업, PINECONE 테스트 코드 리팩토링,
|        | AWS 클라우드에 인프라 구성, 클라우드/온라인에 데이터 Migration 및 코드 배포 |
| 이수미 | HTML, CSS, Javascript 활용 프론트 웹페이지 구현, PINECONE VectorDB 구축, 연동 |
| 김재우 | 웹페이지 구현, AWS 클라우드에 인프라 구성           |
| 정유진 | PPT, README 문서화, 노션-프로젝트 기록           |

---

## 1. 프로젝트 개요


### 1.1 프로젝트명

---

워시톡 (WashTalk) - 이미지 기반 세탁기/건조기 Q&A 챗봇 시스템

### 1.2 목적

---

사용자가 세탁기/건조기에 대한 궁금한 점을 손쉽게 해결할 수 있는 이미지 기반 Q&A 서비스 제공

### 1.3 범위

---

- 채팅 인터페이스
- 사용자 인증 및 관리
- 대화 히스토리 관리
- 이미지 업로드
- 매뉴얼 PDF 다운로드
- 음성 인터페이스

## 2. 기능 요구사항

### 2.1 사용자 인증 기능

---

- **회원가입**: 이메일, 비밀번호를 통한 회원가입
- **로그인**: 등록된 이메일과 비밀번호로 로그인
- **로그아웃**: 안전한 로그아웃 기능
- **비밀번호 찾기**: 이메일을 통한 비밀번호 재설정

### 2.2 채팅 기능

---

- **챗봇 응답**: 세탁기 관련 질문에 대한 자동 응답
- **메시지 타입**: 텍스트, 이미지, 파일 첨부 지원
- **타이핑 표시**: 챗봇이 응답을 생성 중임을 표시

### 2.3 대화 관리 기능

---

- **대화 목록**: 사용자별 대화 세션 목록 표시
- **대화 히스토리**: 과거 대화 내용 조회 및 검색
- **대화 삭제**: 불필요한 대화 세션 삭제

### 2.4 파일 관리 기능

---

- **파일 업로드**: 이미지 파일 업로드 지원
- **매뉴얼 다운로드**: 매뉴얼 pdf 다운로드

## 3. 데이터베이스 설계

### 3.1 주요 테이블
<img width="50" height="39" alt="image" src="https://github.com/user-attachments/assets/ef367d0e-60f4-4044-b08a-f7e398a76c72" />

---

- **users**: 사용자 정보
- **conversations**: 대화 세션
- **messages**: 메시지 내용
- **files**: 업로드 파일 정보
- **chat_history**: 채팅 히스토리 

---
 <img width="53" height="73" alt="image" src="https://github.com/user-attachments/assets/31aaf209-7f1b-49ed-ab8b-874bc6436582" />


---
## 4. 개발/협업 프로세스
<img width="123" height="39" alt="image" src="https://github.com/user-attachments/assets/ec6f4dc8-0828-43ca-959b-5ceeda4874e3" />

- **스크럼 방식**:
    - Notion+Github, Discord 기반 데일리 진행
    - 역할별(데이터/모델/프론트/문서) Task 세분화
    - PR, 코드리뷰 사용

### **■ 개발 환경**:

- Google Colab, Pycharm, VSCode
- **언어**: Python
- **프레임워크**: Django
- **데이터베이스**: MySQL + Pinecone
- **웹서버**: Nginx + Gunicorn

### **■ 배포 환경:**

- **서버**: Linux (Ubuntu)
- **컨테이너**: Docker + Docker Compose
- **기술 스택**: OpenAI, Huggingface, MySQL, Pinecone, Langchain, django, Tavily, Gamma, Docker, Docker Compose
<img width="75" height="38" alt="image" src="https://github.com/user-attachments/assets/3750fd6d-90bf-4d14-9bef-c12dc4b47398" />

## 5. 화면 구성 

<img width="78" height="53" alt="image" src="https://github.com/user-attachments/assets/35881bd7-b5da-43d7-b223-c6a4aca873a6" />
<img width="75" height="52" alt="image" src="https://github.com/user-attachments/assets/e8a6f6e9-adb6-4783-aedb-957fba160f77" />
<img width="79" height="56" alt="image" src="https://github.com/user-attachments/assets/7888185b-f766-46fe-8f40-78ddce698b2c" />
<img width="186" height="91" alt="image" src="https://github.com/user-attachments/assets/a134bed9-90be-43ff-95e4-dd144560cb76" />

- 이미지 업로드 및 질문 입력, 대화 기록 저장 및 삭제, 사용자 이미지 기반 모델명 인식, 모델명 & 사용자 질문 기반 답변 생성 


---

## 6. 기대효과

- **고객지원**: 고객이 입력하는 질문에 대해 고장, 사용법, 청소방법 등 바로 안내
- **고객센터/마케팅**: 24시간 자동응대 및 빠른 상담 처리를 통한 운영 비용 절감
- **서비스 확장성**: 이미지/텍스트 입력 방식으로 사용자 경험 극대화
- **시장 확장성**: 다국어 지원, 다양한 브랜드 및 제품군 확장으로 고객 커버리지 확대

---

## 7. 한 줄 회고 

- **유용환**: 사용자 질문과 이미지를 결합해 실질적인 정보를 제공하는 RAG 시스템을 직접 구현해보고, 데이터 처리부터 LLM 응답 생성과정까지 좀 더 깊은 이해를 할 수 있었던 것 같습니다.
- **윤이서**: 웹 구조에 대한 이해를 확장하고 체계적인 데이터 수집 경험을 쌓을 수 있었으며, 짧은 시간 내 LLM/RAG 시스템을 함께 완성해낸 팀원들 덕분에 더욱 의미 있는 성장의 시간을 보낼 수 있었습니다.
- **김준기**: 배운 내용을 프로젝트에 실제로 적용하는 과정을 통해 백터디비 구축과 실제 챗봇이 어떻게 구성되 있는지 그 과정을 잘 이해할 수 있었습니다.
- **이수미**: RAG 서비스 처음 만들어보았는데, 팀원분들과 협력하고 구현하는 과정 중에 많은 배움과 이해를 얻어갈 수 있었습니다. 더욱 복합적인 웹 서비스로 발전시켜보고 싶습니다.
- **김재우**: 난이도가 높은 팀플 과제 였지만 협력을 통해 문제점을 하나씩 고쳐가면서 완성하는 과정이 좋았고 스트림릿 UI를 더 복합적으로 만들 수 있게 되었다.
- **정유진**: 팀 단위로 LLM/RAG 실습 및 프로젝트 준비과정을 통해 유익한 경험을 할 수 있었습니다.

---

## 8. 참고 자료 및 활용 코드

- [프로젝트 노션] https://www.notion.so/shqkel/SKN14-4th-3-2429cb46e5e28053aa58ed039a751aa7?source=copy_link
- [GitHub 저장소] https://github.com/skn-ai14-250409/SKN14-4th-3Team
  
---



