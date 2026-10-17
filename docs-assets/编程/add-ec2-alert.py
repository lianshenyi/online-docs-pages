#!/usr/bin/python
# -*- coding: utf-8 -*-


import json
import subprocess

# aws-cli 地址
Contants = {
    "AWSCLI": "/usr/local/bin/aws",
    "AWSREGION": ['cn-northwest-1']  # 宁夏
}

# 构造字典
class CreateDict(dict):
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

#########################################################################################################
# 配置告警

# CPUUtilization,15分钟检查3次，平均值大于或等于80%，就告警。
def getCPUUtilizationComm(name, action, instance_id, ip):
    mertic = 'CPUUtilization'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "EC2_{name}_{ip}_{mertic} >= 80%" \
--alarm-description "aws ec2 {mertic}" \
--metric-name {mertic} \
--namespace AWS/EC2 \
--statistic Maximum \
--period 300 \
--threshold 80 \
--evaluation-periods 1 \
--datapoints-to-alarm 1 \
--comparison-operator GreaterThanOrEqualToThreshold \
--treat-missing-data notBreaching \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--unit Percent \
--dimensions "Name=InstanceId,Value={id}"'''.format(cli=Contants['AWSCLI'], name=name, action=action, id=instance_id, mertic=mertic, ip=ip)

# NetworkIn,15分钟检查3次，平均值大于或等于1G，就告警。
def getNetworkInComm(name, action, instance_id, ip):
    mertic = 'NetworkIn'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "EC2_{name}_{ip}_{mertic} > 1G" \
--alarm-description "aws ec2 {mertic}" \
--metric-name {mertic} \
--namespace AWS/EC2 \
--statistic Average \
--period 300 \
--threshold 1000000000 \
--evaluation-periods 3 \
--datapoints-to-alarm 3 \
--comparison-operator GreaterThanOrEqualToThreshold \
--treat-missing-data notBreaching \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions "Name=InstanceId,Value={id}"'''.format(cli=Contants['AWSCLI'], name=name, action=action, id=instance_id, mertic=mertic, ip=ip)

# NetworkOut,3分钟检查3次，平均值大于或等于5m，就告警。
def getNetworkOutComm(name, action, instance_id, ip):
    mertic = 'NetworkOut'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "EC2_{name}_{ip}_{mertic} > 1G" \
--alarm-description "aws ec2 {mertic}" \
--metric-name {mertic} \
--namespace AWS/EC2 \
--statistic Average \
--period 300 \
--threshold 10000000 \
--evaluation-periods 3 \
--datapoints-to-alarm 3 \
--comparison-operator GreaterThanOrEqualToThreshold \
--treat-missing-data notBreaching \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions "Name=InstanceId,Value={id}"'''.format(cli=Contants['AWSCLI'], name=name, action=action, id=instance_id, mertic=mertic, ip=ip)

# Memory,15分钟检查3次，平均值大于或等于90，就告警。
def getMemoryComm(name, action, instance_id, ip):
    mertic = 'mem_used_percent'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "EC2_{name}_{ip}_Memory > 80%" \
--alarm-description "aws ec2 {mertic}" \
--metric-name {mertic} \
--namespace CWAgent \
--statistic Average \
--period 300 \
--threshold 80 \
--evaluation-periods 3 \
--datapoints-to-alarm 3 \
--comparison-operator GreaterThanOrEqualToThreshold  \
--treat-missing-data notBreaching \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions "Name=InstanceId,Value={id}"'''.format(cli=Contants['AWSCLI'],  name=name, action=action,
                                                              id=instance_id, mertic=mertic, ip=ip)

# 根盘,15分钟检查3次，平均值大于或等于90，就告警。
def getDiskUsedComm(name, action, instance_id, ip):
    mertic = 'disk_used_percent'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "EC2_{name}_{ip}-Disk-/ > 80%" \
--alarm-description "aws ec2 / {mertic}" \
--metric-name {mertic} \
--namespace CWAgent \
--statistic Average \
--period 300 \
--threshold 80 \
--evaluation-periods 3 \
--datapoints-to-alarm 3 \
--comparison-operator GreaterThanOrEqualToThreshold  \
--treat-missing-data notBreaching \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions "Name=InstanceId,Value={id}" "Name=path,Value=/" "Name=device,Value=nvme0n1p1" "Name=fstype,Value=xfs"'''.format(cli=Contants['AWSCLI'], name=name, action=action,
                                                              id=instance_id, mertic=mertic, ip=ip)

# 额外盘,15分钟检查3次，平均值大于或等于90，就告警。
def getbackupDiskUsedComm(name, action, instance_id, ip):
    mertic = 'disk_used_percent'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "EC2_{name}_{ip}-Disk-/backup > 80%" \
--alarm-description "aws ec2 /backup {mertic}" \
--metric-name {mertic} \
--namespace CWAgent \
--statistic Average \
--period 300 \
--threshold 80 \
--evaluation-periods 3 \
--datapoints-to-alarm 3 \
--comparison-operator GreaterThanOrEqualToThreshold  \
--treat-missing-data notBreaching \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions "Name=InstanceId,Value={id}" "Name=path,Value=/backup" "Name=device,Value=nvme1n1" "Name=fstype,Value=ext4"'''.format(cli=Contants['AWSCLI'], name=name, action=action,
                                                              id=instance_id, mertic=mertic, ip=ip)

# 额外盘,15分钟检查3次，平均值大于或等于90，就告警。
def getdataDiskUsedComm(name, action, instance_id, ip):
    mertic = 'disk_used_percent'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "EC2_{name}_{ip}-Disk-/data > 80%" \
--alarm-description "aws ec2 /data {mertic}" \
--metric-name {mertic} \
--namespace CWAgent \
--statistic Average \
--period 300 \
--threshold 80 \
--evaluation-periods 3 \
--datapoints-to-alarm 3 \
--comparison-operator GreaterThanOrEqualToThreshold  \
--treat-missing-data notBreaching \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions "Name=InstanceId,Value={id}" "Name=path,Value=/data" "Name=device,Value=nvme1n1" "Name=fstype,Value=ext4"'''.format(cli=Contants['AWSCLI'], name=name, action=action,
                                                              id=instance_id, mertic=mertic, ip=ip)

# CWAgent
# disk_used_percent
# path: /backup
# InstanceId: i-00a57533316c6901b
# device: nvme1n1
# fstype: ext4

# NetworkIn,15分钟检查3次，平均值大于或等于1G，就告警。
def getStatusCheckFailedComm(name, action, instance_id, ip):
    mertic = 'StatusCheckFailed'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "EC2_{name}_{ip} = Unhealthy" \
--alarm-description "aws ec2 {mertic}" \
--metric-name {mertic} \
--namespace AWS/EC2 \
--statistic Sum \
--period 300 \
--threshold 1 \
--evaluation-periods 1 \
--datapoints-to-alarm 1 \
--comparison-operator GreaterThanOrEqualToThreshold \
--treat-missing-data notBreaching \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions "Name=InstanceId,Value={id}"'''.format(cli=Contants['AWSCLI'], name=name, action=action, id=instance_id, mertic=mertic, ip=ip)

# NetworkIn,15分钟检查3次，平均值大于或等于1G，就告警。
def getEBSWriteOpsComm(name, action, instance_id, ip, iops):
    mertic = 'EBSWriteOps'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "EC2_{name}_{ip}_{mertic} >= {value}" \
--alarm-description "aws ec2 {mertic}" \
--metric-name {mertic} \
--namespace AWS/EC2 \
--statistic Sum \
--period 300 \
--threshold {value} \
--evaluation-periods 1 \
--datapoints-to-alarm 1 \
--comparison-operator GreaterThanOrEqualToThreshold \
--treat-missing-data notBreaching \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions "Name=InstanceId,Value={id}"'''.format(cli=Contants['AWSCLI'], name=name, action=action, id=instance_id, mertic=mertic, ip=ip, value=int(iops*300/2))


def getEBSReadOpsComm(name, action, instance_id, ip, iops):
    mertic = 'EBSReadOps'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "EC2_{name}_{ip}_{mertic} >= {value}" \
--alarm-description "aws ec2 {mertic}" \
--metric-name {mertic} \
--namespace AWS/EC2 \
--statistic Sum \
--period 300 \
--threshold {value} \
--evaluation-periods 1 \
--datapoints-to-alarm 1 \
--comparison-operator GreaterThanOrEqualToThreshold \
--treat-missing-data notBreaching \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions "Name=InstanceId,Value={id}"'''.format(cli=Contants['AWSCLI'], name=name, action=action, id=instance_id, mertic=mertic, ip=ip, value=int(iops*300/2))


450000

# 执行命令函数
def execCommand(comm):
    try:
        print(comm)
        (status, stdout) = subprocess.getstatusoutput(comm)
        print(status)
        return stdout
    except Exception as e:
        print(e)

# 获取当前可用区内所有lb2的基础信息
def getAll():
    comm1 = "%s ec2 describe-instances" % Contants['AWSCLI']
    all_data = json.loads(execCommand(comm1))
    instance_list = []

    for r in all_data['Reservations']:
        for i in r['Instances']:
            data = {'id': i['InstanceId'], 'ip': i['PrivateIpAddress']}
            for t in i['Tags']:
                if t['Key'] == 'Name':
                    data['name'] = t['Value']
            if 'name' not in data:
                data['name'] = i['InstanceId']
            instance_list.append(data)

    return instance_list

# 获取指定 EC2
def ec2_list():
    ec2 = [
        {
            "name": "PRD-ZHY-AS-EC2-APIAERVER-GOLANG-01",
            "id": "i-00a57533316c6901b",
            "ip": "10.172.0.194"
        },
        {
            "name": "PRD-ZHY-AS-EC2-APIAERVER-GOLANG-02",
            "id": "i-004a73e2b9a618a5e",
            "ip": "10.172.6.177"
        },
        {
            "name": "PRD-ZHY-AS-EC2-APIAERVER-GOLANG-03",
            "id": "i-03b12e6cf19709001",
            "ip": "10.172.9.143"
        },
    ]
    return ec2

def gp_list():
    ec2 = [
        {
            "name": "PRD-ZHY-AS-DWS-GP1",
            "id": "i-0dd3510beb0bd8430",
            "ip": "10.172.17.197"
        },
        {
            "name": "PRD-ZHY-AS-DWS-GP2",
            "id": "i-024cd002fa4bc8204",
            "ip": "10.172.17.232"
        },
        {
            "name": "PRD-ZHY-AS-DWS-GP3",
            "id": "i-0f9ae76b3ec274ef6",
            "ip": "10.172.17.73"
        },
    ]
    return ec2

def zk_list():
    ec2 = [
        {
            "name": "PRD-ZHY-AS-DWS-ZK1",
            "id": "i-0af27cd81e9794a66",
            "ip": "10.172.15.173"
        },
        {
            "name": "PRD-ZHY-AS-DWS-ZK2",
            "id": "i-0138a98ea5c0c7ee4",
            "ip": "10.172.15.125"
        },
        {
            "name": "PRD-ZHY-AS-DWS-ZK3",
            "id": "i-08880aa6f3ebfd307",
            "ip": "10.172.15.70"
        },
    ]
    return ec2

# 添加报警
def add_alert(data, action):
    for i in data:
        print(i)
        instance_id = i['id']
        name = i['name']
        # print(name)
        ip = i['ip']
        iops = 3000
        # execCommand(getCPUUtilizationComm(name, action, instance_id, ip))
        # execCommand(getEBSWriteOpsComm(name, action, instance_id, ip, iops))
        # execCommand(getEBSReadOpsComm(name, action, instance_id, ip, iops))
        execCommand(getStatusCheckFailedComm(name, action, instance_id, ip))

        # execCommand(getNetworkInComm(name, action, instance_id, ip))
        # execCommand(getNetworkOutComm(name, action, instance_id, ip))
        # execCommand(getMemoryComm(name, action, instance_id, ip))
        # # execCommand(getDiskUsedComm(name, action, instance_id, ip))
        # execCommand(getbackupDiskUsedComm(name, action, instance_id, ip))
        # execCommand(getdataDiskUsedComm(name, action, instance_id, ip))


if __name__ == '__main__':
    # 2. 配置sns的arn
    sns_arn = "arn:aws-cn:sns:cn-northwest-1:182411574528:test"
    cli = Contants['AWSCLI']
    for i in Contants['AWSREGION']:
        Contants['AWSCLI'] = cli + ' --region ' + i
        add_alert(getAll(), sns_arn)
        # add_alert(zk_list(), sns_arn)
