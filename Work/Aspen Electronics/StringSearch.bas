' String Search
' By J. Ashmore
' August 3, 2017

' Sifts through all text files in a folder for a given string

#Include "dir.bi"
Declare Sub SearchString
Declare Sub WalkDir(ByRef filespec as String)
Declare Sub ReadFiles
Declare Sub Results
Declare sub clearall

Dim Shared folder As String
Dim Shared toSearch as String
Dim Shared Filenames() as String
Dim Shared count as Integer
Dim Shared found() as String 'File path array, used if text is found
Dim Shared foundCount as Integer = 0
Dim Shared check as String
Dim Shared lineNums(0 TO 1000000) as String
Dim Shared lineCount as Integer = 0
Dim Shared repeat as Integer  = 1
folder = "C:\Test\"
toSearch = ""

print ""
print "Searching in folder: " + folder
WalkDir(folder & "*.*")
print "Files: " + str(count)

SearchString

'--------------------------------------------------------------'

Sub SearchString()
    Dim yn as String
    While (repeat > 0)
        print ""
        Input "Please Enter a String to Search" ; toSearch
        If LCase(toSearch) = "quit" Then
            Exit Sub
        End If
        print ""
        print "Searching..."
        print ""
        ReadFiles
        If foundCount > 0 Then
            
            print "----------------------------------------------------"
            print ""
            Results
            print "----------------------------------------------------"
        Else
            print "----------------------------------------------------"
            print ""
            print "No results found!"
            print ""
            print "----------------------------------------------------"
        End If
        print ""
        Input "Search again Y/N" ; yn
        If LCase(yn) = "y" Then
            clearall
        Else repeat = 0
        End if
    Wend
End Sub

'--------------------------------------------------------------'

Sub WalkDir(ByRef filespec as String)
    count = 0: ReDim Filenames(0) as String
    If Len(Dir(filespec)) = 0 Then
        Exit Sub
    End If
    Do
        count += 1
    Loop While Len(Dir()) > 0
    ReDim Filenames(count) as String
    Filenames(1) = Dir(filespec,fbNormal)
    For I as Integer = 2 To count
        Filenames(I) = Dir()
    Next I    
    
End Sub

'--------------------------------------------------------------'


Sub ReadFiles()
    Dim a as integer
    ReDim found(count) As String
    For a = 0 To count
        Dim Filehandle As Integer = FreeFile
        Open str(folder & Filenames(a)) for Input As #filehandle
        Do Until EOF(filehandle)
            lineCount += 1
            Line Input #filehandle, check
            If Len(check) > 0 And InStr(LCase(check), LCase(toSearch)) <> 0 Then
                found(foundCount) = str(folder & Filenames(a))
                foundCount += 1
                lineNums(foundCount) += str(lineCount) + " "
            End If
        Loop
        Close #filehandle
        lineCount = 0
    Next a
End Sub

'--------------------------------------------------------------'

Sub Results()
    print "Found: " + str(foundCount) + " results in the following files:"
    print ""
    Dim b as Integer
    for b = 0 To foundCount
        if b > 0 Then
            If found(b) <> found(b-1) Then
                print found(b)
            End If
        ElseIf found(b) <> "" Then
            print found(b)
        End If
        If lineNums(b+1) <> "" Then
            print "Line: " + lineNums(b+1)
        End If
    next b
End Sub

'-----------------------------------------------------------'

Sub clearall()
    Dim Filenames() As String
    Erase lineNums
    Erase found
    Dim count As Integer = 0
    Dim foundCount As Integer  = 0
    Dim lineCount As Integer  = 0
    Dim toSearch As String
End Sub
    