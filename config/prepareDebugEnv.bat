cd %~dp0
mklink /H ..\build\Debug_Win32\omniORB421_vc14_rtd.dll ..\thirdparty\omniORB-4.2.1\bin\x86_win32\omniORB421_vc14_rtd.dll
mklink /H ..\build\Debug_Win32\omniDynamic421_vc14_rtd.dll ..\thirdparty\omniORB-4.2.1\bin\x86_win32\omniDynamic421_vc14_rtd.dll
mklink /H ..\build\Debug_Win32\omnithread40_vc14_rtd.dll ..\thirdparty\omniORB-4.2.1\bin\x86_win32\omnithread40_vc14_rtd.dll

mklink /H ..\build\Debug_Win32\omniORB421_vc14_rtd.pdb ..\thirdparty\omniORB-4.2.1\bin\x86_win32\omniORB421_vc14_rtd.pdb
mklink /H ..\build\Debug_Win32\omniDynamic421_vc14_rtd.pdb ..\thirdparty\omniORB-4.2.1\bin\x86_win32\omniDynamic421_vc14_rtd.pdb
mklink /H ..\build\Debug_Win32\omnithread40_vc14_rtd.pdb ..\thirdparty\omniORB-4.2.1\bin\x86_win32\omnithread40_vc14_rtd.pdb

SET OMNIORB_CONFIG="%~dp0omniORB.cfg"