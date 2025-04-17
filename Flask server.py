from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import pymysql

app = Flask(__name__)

# MySQL 데이터베이스 연결 정보
MYSQL_HOST = 'hostName'
MYSQL_USER = 'userName'
MYSQL_PASSWORD = 'passwordName'
MYSQL_DB = 'dbName'

# MySQL 연결 (PyMySQL 사용)
def get_db_connection():
    connection = pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        db=MYSQL_DB,
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor  # 쿼리 결과를 딕셔너리로 가져오기 위해 설정
    )
    return connection

def execute_query(query, params=None, fetchone=False, commit=False):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params or ())
            if commit:
                connection.commit()
            if fetchone:
                return cursor.fetchone()
            else:
                return cursor.fetchall()
    finally:
        connection.close()


@app.route('/')
def boardMain():
    return render_template('boardMain.html')


# 게시판 목록 페이지 라우트
@app.route('/boardList')
def boardList():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # 게시글 목록 쿼리 실행
            query = "SELECT * FROM BOARD"
            cursor.execute(query)
            boardList = cursor.fetchall()  # 모든 게시글 데이터를 가져옴
    finally:
        connection.close()

    # boardList.html 템플릿으로 전달
    return render_template('boardList.html', boardList=boardList)

# 게시글 작성 페이지 라우트
@app.route('/board/createBoard', methods=['GET', 'POST'])
def createBoard():
    if request.method == 'POST':
        # POST 요청 시, 폼 데이터 받기
        writer = request.form['writer']
        subject = request.form['subject']
        passwd = request.form['passwd']
        content = request.form['content']
        
        # DB 연결 후 데이터 삽입
        query = """
        INSERT INTO board (writer, subject, passwd, content)
        VALUES (%s, %s, %s, %s)
        """
        execute_query(query, (writer, subject, passwd, content), commit=True)

        # 게시글 목록 페이지로 리디렉션
        return redirect(url_for('boardList'))
    
    return render_template('createBoard.html')


# 게시글 상세 페이지를 처리하는 라우트
@app.route('/board/boardDetail', methods=['GET'])
def boardDetail():

    # URL 파라미터에서 boardId를 가져옴
    boardId = request.args.get('boardId')  # 요청 파라미터에서 boardId 값을 받음

    # DB 연결 후 데이터 삽입
    query = """
        SELECT * 
        FROM BOARD 
        WHERE BOARD_ID = %s
    """   
    query_update_read_cnt = """
        UPDATE BOARD
        SET READ_CNT = READ_CNT + 1
        WHERE BOARD_ID = %s
    """

    # READ_CNT 증가
    execute_query(query_update_read_cnt, (boardId), commit=True)  
    
    # 게시글을 템플릿에 전달
    boardDTO = execute_query(query, (boardId), fetchone=True)

    # 게시글 목록 페이지로 리디렉션
    return render_template('boardDetail.html', boardDTO=boardDTO)


@app.route('/authentication', methods=['GET', 'POST'])
def authentication():
    if request.method == 'POST':

        boardId = request.form['boardId']  # 폼에서 boardId 가져오기
        passwd = request.form['passwd']   # 폼에서 password 가져오기
        menu = request.form['menu']        # 폼에서 menu 가져오기
       
        query = "SELECT * FROM BOARD WHERE BOARD_ID = %s"
        boardDTO = execute_query(query, (boardId,), fetchone=True)
 
        if passwd == boardDTO['PASSWD']:
            delete_query = """
                    DELETE FROM BOARD 
                    WHERE BOARD_ID = %s
                    """
            execute_query(delete_query, (boardId,), commit=True)  # 삭제 쿼리 실행
            return redirect(url_for('boardList'))
        else:
                # 패스워드가 맞지 않으면 오류 메시지 출력
            jsScript = """
                <script>
                        alert('패스워드를 확인하세요.');
                        history.go(-1);
                    </script>
                """
            return jsScript


    boardId = request.args.get('boardId')
   
    query = """
        SELECT * 
        FROM BOARD 
        WHERE BOARD_ID = %s
    """  
    # 게시글을 템플릿에 전달
    boardDTO = execute_query(query, (boardId), fetchone=True)

    # 게시글 목록 페이지로 리디렉션
    return render_template('authentication.html', boardDTO=boardDTO)


if __name__ == '__main__':
    app.run(debug=True)
