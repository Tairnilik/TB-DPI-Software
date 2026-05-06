:fool
@echo off
set /p fooling_Mode="Enter one of these options (md5sig, badseq, badsum, datanoack): "

if "%fooling_Mode%"=="md5sig" (
    echo md5sig> fooling.mode
) else if "%fooling_Mode%"=="badseq" (
    echo badseq> fooling.mode
) else if "%fooling_Mode%"=="badsum" (
    echo badsum> fooling.mode
) else if "%fooling_Mode%"=="datanoack" (
    echo datanoack> fooling.mode
) else (
    echo Error: Invalid option selected.
    pause
    goto fool
)

echo Done.
pause