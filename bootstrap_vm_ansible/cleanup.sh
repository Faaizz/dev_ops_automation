source vars.sh

VBoxManage unregister $NAME && \
rm -rf $NAME/ $NAME.vdi || true
