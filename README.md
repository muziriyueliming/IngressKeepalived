12.1. 高可靠概念
　　HA(High Available)：高可用性集群，是保证业务连续性的有效解决方案，一般有两个或两个以上的节点，且分为活动节点及备用节点。
　

2.2. 高可靠软件keepalived
　　keepalive是一款可以实现高可靠的软件，通常部署在2台服务器上，分为一主一备。Keepalived可以对本机上的进程进行检测，一旦Master检测出某个进程出
现问题，将自己切换成Backup状态，然后通知另外一个节点切换成Master状态。
2.3. keepalived安装
　　下载keepalived官网：http://keepalived.org
yum -y install libnl libnl-devel libnfnetlink-devel wget openssl openssl-devel gcc-c++ -y
wget -O /opt/keepalived-2.0.18.tar.gz https://keepalived.org/software/keepalived-2.0.18.tar.gz

　　 将keepalived解压到/usr/local/src目录下：
cd /opt/ && tar -zxvf keepalived-2.0.18.tar.gz && cd keepalived-2.0.18


 开始configure（检查安装环境,并指定将来要安装的路径）：
./configure --prefix=/usr/local/keepalived

　　 #编译并安装：
make && make install

2.4. 将keepalived添加到系统服务中　　
　　拷贝执行文件：
ln -s /usr/local/keepalived/sbin/keepalived /usr/sbin/

　　将init.d文件拷贝到etc下，加入开机启动项：
cp ./keepalived/etc/init.d/keepalived /etc/init.d/keepalived　

　　将keepalived文件拷贝到etc下：
ln -s /usr/local/keepalived/etc/sysconfig/keepalived /etc/sysconfig/　

　　创建keepalived文件夹：
mkdir -p /etc/keepalived

　　将keepalived配置文件拷贝到etc下：
cp /usr/local/keepalived/etc/keepalived/keepalived.conf /etc/keepalived/keepalived.conf　

　　添加可执行权限：
chmod +x /etc/init.d/keepalived

　　添加keepalived到开机启动：
chkconfig --add keepalived && chkconfig keepalived on