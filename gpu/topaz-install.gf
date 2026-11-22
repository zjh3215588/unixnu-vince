run
mount-options rw,force /dev/sda /
mkdir-p /topaz/lib
copy-in /root/ref/topaz-artifacts/mesa-ios/libOSMesa.8.dylib /topaz/lib
copy-in /root/ref/topaz-artifacts/topaz-ios/libtopaz-gl.dylib /topaz/lib
copy-in /root/ref/topaz-artifacts/topaz-ios/libtopaz-inject.dylib /topaz/lib
chmod 0755 /topaz/lib/libOSMesa.8.dylib
chmod 0755 /topaz/lib/libtopaz-gl.dylib
chmod 0755 /topaz/lib/libtopaz-inject.dylib
chown 0 0 /topaz/lib/libOSMesa.8.dylib
chown 0 0 /topaz/lib/libtopaz-gl.dylib
chown 0 0 /topaz/lib/libtopaz-inject.dylib
mkdir-p /usr/libexec/real
mv /usr/libexec/backboardd /usr/libexec/real/backboardd
copy-in /root/ref/topaz-artifacts/topaz-ios/backboardd-wrap /usr/libexec
mv /usr/libexec/backboardd-wrap /usr/libexec/backboardd
chmod 0755 /usr/libexec/backboardd
chown 0 0 /usr/libexec/backboardd
mkdir-p /usr/local/bin
copy-in /root/ref/topaz-artifacts/mesa-ios/gputest /usr/local/bin
mv /usr/local/bin/gputest /usr/local/bin/vince-gputest
chmod 0755 /usr/local/bin/vince-gputest
chown 0 0 /usr/local/bin/vince-gputest
copy-in /root/ref/topaz-artifacts/launchd.plist.gpu /System/Library/xpc
mv /System/Library/xpc/launchd.plist.gpu /System/Library/xpc/launchd.plist
chmod 0644 /System/Library/xpc/launchd.plist
chown 0 0 /System/Library/xpc/launchd.plist
ls /topaz/lib
ls /usr/libexec/real
ls /usr/local/bin
