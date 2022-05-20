source vars.sh

echo "Create VM" && \
VBoxManage createvm --name $NAME --ostype Ubuntu_64 --basefolder $BASE_FOLDER --register && \
echo "Created VM..." && \
 \
echo "Create Storage Medium" && \
VBoxManage createmedium --filename "$BASE_FOLDER/$NAME.vdi" --size $MD_SIZE && \
echo "Created Storage Medium..." && \
 \
echo "Attach SATA Storage  \Controller" && \
VBoxManage storagectl $NAME --name SATA --add SATA --controller IntelAhci  && \
VBoxManage storageattach $NAME --storagectl SATA --port 0 --device 0 --type hdd --medium "$BASE_FOLDER/$NAME.vdi" && \
echo "Created SATA Controller & Mounted Storage Medium..." && \
 \
echo "Attach IDE Storage Controller to mount installation disk image" && \
VBoxManage storagectl $NAME --name IDE --add ide && \
VBoxManage storageattach $NAME --storagectl IDE --port 0 --device 0 --type dvddrive --medium $INSTALL_DISK_IMG_PATH && \
echo "Created IDE Controller & Mounted Disk Image..." && \
 \
echo "Set RAM and nvram size" && \
VBoxManage modifyvm $NAME --memory $RAM --vram $NVRAM && \
echo "Configured RAM..." && \
 \
echo "Enable IO APIC -- such that the guest OS can use more than 16 interrupt requests IRQ to avoid IRQ sharing" && \
VBoxManage modifyvm $NAME --ioapic on && \
echo "Configured IO APIC..." && \
 \
echo "Define boot order" && \
VBoxManage modifyvm $NAME --boot1 dvd --boot2 disk --boot3 none --boot4 none && \
echo "Configured Boot Order..." && \
 \
echo "Define number of virtual CPUs" && \
VBoxManage modifyvm $NAME --cpus $CPUS && \
echo "Configured vCPUs..." && \
 \
echo "Disable Audio" && \
VBoxManage modifyvm $NAME --audio none && \
echo "Configured Audio..." && \
 \
echo "Disbale USB controllers" && \
VBoxManage modifyvm $NAME --usb off && \
VBoxManage modifyvm $NAME --usbehci off && \
VBoxManage modifyvm $NAME --usbxhci off && \
echo "Configured USB Controllers..." && \
 \
echo "Define netwrok settings" && \
VBoxManage modifyvm $NAME --nic1 bridged --bridgeadapter1 wlan0 && \
echo "Configured Network..." && \
 \
echo "Install OS" && \
VBoxManage unattended install $NAME --user=$USER --password=$PASSWORD --country=$COUNTRY --time-zone=$TIMEZONE --hostname=$HOSTNAME --iso=$INSTALL_DISK_IMG_PATH --start-vm=gui && \
echo "Installed OS..."
