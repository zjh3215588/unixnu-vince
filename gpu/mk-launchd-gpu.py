import plistlib
src='/root/ref/topaz-artifacts/root-orig/launchd.plist'
dst='/root/ref/topaz-artifacts/launchd.plist.gpu'
with open(src,'rb') as f: plist=plistlib.load(f)
jobs=plist['LaunchDaemons']
LABEL='com.vince.gputest'
for k in [k for k,j in jobs.items() if j.get('Label')==LABEL]: del jobs[k]
jobs['/System/Library/LaunchDaemons/%s.plist'%LABEL]={
 'Label':LABEL,'ProgramArguments':['/usr/local/bin/vince-gputest'],'RunAtLoad':True,'KeepAlive':False,
 'StandardOutPath':'/dev/console','StandardErrorPath':'/dev/console',
 'JetsamProperties':{'JetsamMemoryLimit':1024},'EnablePressuredExit':False,'EnableTransactions':False}
with open(dst,'wb') as f: plistlib.dump(plist,f,fmt=plistlib.FMT_BINARY)
print('wrote',dst)
