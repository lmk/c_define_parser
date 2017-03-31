# c_define_parser

## 개요
c 헤더 파일을 파싱해서 '#define', 'enum' 구문으로 정의된 값, 상수명을 검색합니다.

## 사용법
error.h 파일의 내용이 아래와 같을 때
```cpp
#define ERROR_NONE 0x00
#define ERROR_LOGIN 0x01
#define ERROR_FILE 0x02
#define ERROR_DEVICE 0x03
```

```bash
$ find_const.py 1
0 is ERROR_LOGIN

$ find_const.py 0x03
0x03 is ERROR_DEVICE
```

## 구현 로직
1. 모든 파일을 머지한다.
2. 주석을 제거한다.
3. enum 구문을 파싱해서 dic_command에 저장한다.
4. define 구문을 파싱해서 dic_command에 저장한다.
5. dic_command에 저장된 상수 값을 찾아서 치환 한다.
6. dic_command의 key, value 값을 바꿔서 dic_command_r에 저장한다.
7. 값으로 상수를 찾는다.