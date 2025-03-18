;
; Simple NSIs test script to verify this Conan recipe 
;

!define /ifndef OUTPUT_PATH "test.exe"

;--------------------------------

Name "Test"

; The file to write
OutFile ${OUTPUT_PATH}

; Request application privileges for Windows Vista
RequestExecutionLevel user

; Build Unicode installer
Unicode True

; The default installation directory
InstallDir $DESKTOP\test

;--------------------------------

; Pages

Page directory
Page instfiles

;--------------------------------

; The stuff to install
Section "" ;No components page, name is not important

  ; Set output path to the installation directory.
  SetOutPath $INSTDIR
  
  ; Put file there
  File test.nsi
  
SectionEnd
