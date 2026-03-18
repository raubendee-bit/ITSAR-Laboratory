@echo off
echo ============================================================
echo   MICROSERVICES CURL TESTING - EVIDENCE FILE
echo ============================================================
echo.

echo ============================================================
echo   STUDENT SERVICE (port 8001)
echo ============================================================
echo.

echo [TEST 1] POST valid student
curl -i -X POST "http://localhost:8001/students" -H "Content-Type: application/json" -d "{\"name\":\"Alice Santos\",\"email\":\"alice@school.com\"}"
echo.
echo ----------------------------------------------------------

echo [TEST 2] POST second valid student
curl -i -X POST "http://localhost:8001/students" -H "Content-Type: application/json" -d "{\"name\":\"Bob Cruz\",\"email\":\"bob@school.com\"}"
echo.
echo ----------------------------------------------------------

echo [TEST 3] GET all students
curl -i "http://localhost:8001/students"
echo.
echo ----------------------------------------------------------

echo [TEST 4] GET student by ID
curl -i "http://localhost:8001/students/1"
echo.
echo ----------------------------------------------------------

echo [TEST 5] EDGE CASE - GET student not found
curl -i "http://localhost:8001/students/999"
echo.
echo ----------------------------------------------------------

echo [TEST 6] EDGE CASE - POST missing fields
curl -i -X POST "http://localhost:8001/students" -H "Content-Type: application/json" -d "{\"name\":\"No Email\"}"
echo.
echo ----------------------------------------------------------

echo [TEST 7] EDGE CASE - POST empty body
curl -i -X POST "http://localhost:8001/students" -H "Content-Type: application/json" -d "{}"
echo.
echo ----------------------------------------------------------

echo [TEST 8] EDGE CASE - POST duplicate email
curl -i -X POST "http://localhost:8001/students" -H "Content-Type: application/json" -d "{\"name\":\"Alice Clone\",\"email\":\"alice@school.com\"}"
echo.
echo ----------------------------------------------------------

echo [TEST 9] DELETE student by ID
curl -i -X DELETE "http://localhost:8001/students/2"
echo.
echo ----------------------------------------------------------

echo [TEST 10] EDGE CASE - DELETE student not found
curl -i -X DELETE "http://localhost:8001/students/999"
echo.
echo ----------------------------------------------------------

echo ============================================================
echo   COURSE SERVICE (port 8002)
echo ============================================================
echo.

echo [TEST 11] POST valid course
curl -i -X POST "http://localhost:8002/courses" -H "Content-Type: application/json" -d "{\"title\":\"Math 101\",\"credits\":3}"
echo.
echo ----------------------------------------------------------

echo [TEST 12] POST second valid course
curl -i -X POST "http://localhost:8002/courses" -H "Content-Type: application/json" -d "{\"title\":\"Programming 101\",\"credits\":5}"
echo.
echo ----------------------------------------------------------

echo [TEST 13] GET all courses
curl -i "http://localhost:8002/courses"
echo.
echo ----------------------------------------------------------

echo [TEST 14] GET course by ID
curl -i "http://localhost:8002/courses/1"
echo.
echo ----------------------------------------------------------

echo [TEST 15] EDGE CASE - GET course not found
curl -i "http://localhost:8002/courses/999"
echo.
echo ----------------------------------------------------------

echo [TEST 16] EDGE CASE - POST missing fields
curl -i -X POST "http://localhost:8002/courses" -H "Content-Type: application/json" -d "{\"title\":\"No Credits\"}"
echo.
echo ----------------------------------------------------------

echo [TEST 17] EDGE CASE - POST invalid credits
curl -i -X POST "http://localhost:8002/courses" -H "Content-Type: application/json" -d "{\"title\":\"Bad Credits\",\"credits\":0}"
echo.
echo ----------------------------------------------------------

echo [TEST 18] EDGE CASE - POST empty body
curl -i -X POST "http://localhost:8002/courses" -H "Content-Type: application/json" -d "{}"
echo.
echo ----------------------------------------------------------

echo [TEST 19] EDGE CASE - DELETE course not found
curl -i -X DELETE "http://localhost:8002/courses/999"
echo.
echo ----------------------------------------------------------

echo ============================================================
echo   ENROLLMENT SERVICE (port 8003)
echo ============================================================
echo.

echo [TEST 20] POST valid enrollment
curl -i -X POST "http://localhost:8003/enrollments" -H "Content-Type: application/json" -d "{\"student_id\":1,\"course_id\":1}"
echo.
echo ----------------------------------------------------------

echo [TEST 21] POST second valid enrollment
curl -i -X POST "http://localhost:8003/enrollments" -H "Content-Type: application/json" -d "{\"student_id\":1,\"course_id\":2}"
echo.
echo ----------------------------------------------------------

echo [TEST 22] GET all enrollments
curl -i "http://localhost:8003/enrollments"
echo.
echo ----------------------------------------------------------

echo [TEST 23] GET enrollment by ID
curl -i "http://localhost:8003/enrollments/1"
echo.
echo ----------------------------------------------------------

echo [TEST 24] EDGE CASE - GET enrollment not found
curl -i "http://localhost:8003/enrollments/999"
echo.
echo ----------------------------------------------------------

echo [TEST 25] EDGE CASE - Duplicate enrollment
curl -i -X POST "http://localhost:8003/enrollments" -H "Content-Type: application/json" -d "{\"student_id\":1,\"course_id\":1}"
echo.
echo ----------------------------------------------------------

echo [TEST 26] EDGE CASE - Student not found
curl -i -X POST "http://localhost:8003/enrollments" -H "Content-Type: application/json" -d "{\"student_id\":999,\"course_id\":1}"
echo.
echo ----------------------------------------------------------

echo [TEST 27] EDGE CASE - Course not found
curl -i -X POST "http://localhost:8003/enrollments" -H "Content-Type: application/json" -d "{\"student_id\":1,\"course_id\":999}"
echo.
echo ----------------------------------------------------------

echo [TEST 28] EDGE CASE - Missing fields
curl -i -X POST "http://localhost:8003/enrollments" -H "Content-Type: application/json" -d "{\"student_id\":1}"
echo.
echo ----------------------------------------------------------

echo [TEST 29] EDGE CASE - Dependency failure
echo NOTE: Stop StudentService in PowerShell before this test
echo Run: Stop-Job -Name StudentService
pause
curl -i -X POST "http://localhost:8003/enrollments" -H "Content-Type: application/json" -d "{\"student_id\":1,\"course_id\":1}"
echo.
echo ----------------------------------------------------------

echo ============================================================
echo   ALL TESTS COMPLETE
echo ============================================================
echo.
echo To save evidence run: test.bat ^> test-evidence.txt 2^>^&1
