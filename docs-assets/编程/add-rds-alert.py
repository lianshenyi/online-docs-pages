#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import subprocess
import os

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

# CPUUtilization,3分钟检查3次，平均值大于或等于90%，就告警。
def getCPUUtilizationComm(action, instance_id):
    mertic = 'CPUUtilization'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "RDS_{id}_{mertic} >= 80%" \
--alarm-description "aws rds {mertic}" \
--metric-name {mertic} \
--namespace AWS/RDS \
--statistic Maximum \
--period 300 \
--threshold 80 \
--evaluation-periods 1 \
--datapoints-to-alarm 1 \
--comparison-operator GreaterThanOrEqualToThreshold \
--treat-missing-data notBreaching \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions "Name=DBInstanceIdentifier,Value={id}"'''.format(cli=Contants['AWSCLI'], action=action,
                                                              id=instance_id, mertic=mertic)

# FreeableMemory,3分钟检查3次，平均值小于于或等于 20%，就告警。
def getFreeableMemoryComm(action, instance_id, ram):
    mertic = 'FreeableMemory'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "RDS_{id}_{mertic} <= 20%" \
--alarm-description "aws mysql {mertic}" \
--metric-name {mertic} \
--namespace AWS/RDS \
--statistic Maximum \
--period 300 \
--threshold {ram} \
--evaluation-periods 1 \
--datapoints-to-alarm 1 \
--comparison-operator LessThanOrEqualToThreshold  \
--treat-missing-data notBreaching \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--ok-actions "{action}" \
--dimensions "Name=DBInstanceIdentifier,Value={id}"'''.format(cli=Contants['AWSCLI'], action=action,
                                                              id=instance_id, mertic=mertic, ram=int(ram*0.2))

# FreeStorageSpace,15分钟检查3次，平均值小于于或等于20%，就告警。
def FreeStorageSpace(action, instance_id, space):
    mertic = 'FreeStorageSpace'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "RDS_{id}_{mertic} <= 20%" \
--alarm-description "aws mysql {mertic}" \
--metric-name {mertic} \
--namespace AWS/RDS \
--statistic Maximum \
--period 300 \
--threshold {space} \
--evaluation-periods 1 \
--datapoints-to-alarm 1 \
--comparison-operator LessThanOrEqualToThreshold  \
--treat-missing-data notBreaching \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions "Name=DBInstanceIdentifier,Value={id}"'''.format(cli=Contants['AWSCLI'], action=action,
                                                              id=instance_id, mertic=mertic, space=int(space*0.2))

# NetworkTransmitThroughput,15分钟检查3次，平均值大于或等于 700M，就告警。
def getNetworkTransmitThroughputComm(action, instance_id):
    mertic = 'NetworkTransmitThroughput'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "RDS_{id}_{mertic} > 700M" \
--alarm-description "aws mysql {mertic}" \
--metric-name {mertic} \
--namespace AWS/RDS \
--statistic Average \
--period 300 \
--threshold 700000000 \
--evaluation-periods 3 \
--datapoints-to-alarm 3 \
--comparison-operator GreaterThanOrEqualToThreshold  \
--treat-missing-data notBreaching \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions "Name=DBInstanceIdentifier,Value={id}"'''.format(cli=Contants['AWSCLI'], action=action,
                                                              id=instance_id, mertic=mertic)

# NetworkBytesOut,15分钟检查3次，平均值大于或等于 700M，就告警。
def getNetworkReceiveThroughputComm(action, instance_id):
    mertic = 'NetworkReceiveThroughput'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "RDS_{id}_{mertic} > 700M" \
--alarm-description "aws mysql {mertic}" \
--metric-name {mertic} \
--namespace AWS/RDS \
--statistic Average \
--period 300 \
--threshold 700000000 \
--evaluation-periods 3 \
--datapoints-to-alarm 3 \
--comparison-operator GreaterThanOrEqualToThreshold  \
--treat-missing-data notBreaching \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions "Name=DBInstanceIdentifier,Value={id}"'''.format(cli=Contants['AWSCLI'], action=action,
                                                              id=instance_id, mertic=mertic)

# ReadLatency,15分钟检查3次，平均值大于或等于 500ms，就告警。
def getReadLatencyComm(action, instance_id):
    mertic = 'ReadLatency'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "RDS_{id}_{mertic} > 100ms" \
--alarm-description "aws mysql {mertic}" \
--metric-name {mertic} \
--namespace AWS/RDS \
--statistic Average \
--period 300 \
--threshold 0.1 \
--evaluation-periods 3 \
--datapoints-to-alarm 3 \
--comparison-operator GreaterThanOrEqualToThreshold  \
--treat-missing-data notBreaching \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions "Name=DBInstanceIdentifier,Value={id}"'''.format(cli=Contants['AWSCLI'], action=action,
                                                              id=instance_id, mertic=mertic)

# WriteLatency,15分钟检查3次，平均值大于或等于 500ms，就告警。
def getWriteLatencyComm(action, instance_id):
    mertic = 'WriteLatency'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "RDS_{id}_{mertic} > 50ms" \
--alarm-description "aws mysql {mertic}" \
--metric-name {mertic} \
--namespace AWS/RDS \
--statistic Average \
--period 300 \
--threshold 0.05 \
--evaluation-periods 3 \
--datapoints-to-alarm 3 \
--comparison-operator GreaterThanOrEqualToThreshold  \
--treat-missing-data notBreaching \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions "Name=DBInstanceIdentifier,Value={id}"'''.format(cli=Contants['AWSCLI'], action=action,
                                                              id=instance_id, mertic=mertic)

# DatabaseConnections,3分钟检查3次，平均值大于或等于500，就告警。
def getDatabaseConnectionsComm(action, instance_id):
    mertic = 'DatabaseConnections'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "RDS_{id}_{mertic} > 1000" \
--alarm-description "aws mysql {mertic}" \
--metric-name {mertic} \
--namespace AWS/RDS \
--statistic Sum \
--period 300 \
--threshold 1000 \
--evaluation-periods 3 \
--datapoints-to-alarm 3 \
--comparison-operator GreaterThanOrEqualToThreshold \
--treat-missing-data notBreaching \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions "Name=DBInstanceIdentifier,Value={id}"'''.format(cli=Contants['AWSCLI'], action=action,
                                                              id=instance_id, mertic=mertic)

def getDiskQueueDepthComm(action, instance_id):
    mertic = 'DiskQueueDepth'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "RDS_{id}_{mertic} >= 5" \
--alarm-description "aws mysql {mertic}" \
--metric-name {mertic} \
--namespace AWS/RDS \
--statistic Sum \
--period 300 \
--threshold 5 \
--evaluation-periods 1 \
--datapoints-to-alarm 1 \
--comparison-operator GreaterThanOrEqualToThreshold \
--treat-missing-data notBreaching \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions "Name=DBInstanceIdentifier,Value={id}"'''.format(cli=Contants['AWSCLI'], action=action,
                                                              id=instance_id, mertic=mertic)


# 执行命令函数
def execCommand(comm):
    try:
        print(comm)
        (status, stdout) = subprocess.getstatusoutput(comm)
        print(status)
        return stdout
    except Exception as e:
        print(e)


# 获取当前可用区内RDS的基础信息
def getAll():
    comm1 = "%s rds describe-db-instances" % Contants['AWSCLI']
    all_data = json.loads(execCommand(comm1))
    instance_list = []
    for r in all_data['DBInstances']:
        if r['Engine'] == 'mysql':
            if r['DBInstanceClass'] == 'db.m6g.2xlarge' or r['DBInstanceClass'] == 'db.m5.2xlarge':
                ram = 32*1024*1024*1024
            elif r['DBInstanceClass'] == 'db.t2.small':
                ram = 2*1024*1024*1024
            elif r['DBInstanceClass'] == "db.m5.xlarge":
                ram = 16*1024*1024*1024
            elif r['DBInstanceClass'] == 'db.m6g.4xlarge':
                ram = 64*1024*1024*1024
            data = {'id': r['DBInstanceIdentifier'], 'space': int(r['AllocatedStorage']*1024*1024*1024), 'ram': ram}
            instance_list.append(data)
    return instance_list


# 添加报警
def add_alert(data, action):
    for i in data:
        id = i['id']
        space = i['space']
        ram = i['ram']
        # execCommand(getDatabaseConnectionsComm(action, id))
        # execCommand(getReadLatencyComm(action, id))
        # execCommand(getWriteLatencyComm(action, id))
        # execCommand(getNetworkReceiveThroughputComm(action, id))
        # execCommand(getNetworkTransmitThroughputComm(action, id))

        execCommand(getCPUUtilizationComm(action, id))
        execCommand(getFreeableMemoryComm(action, id, ram))
        execCommand(FreeStorageSpace(action, id, space))
        execCommand(getDiskQueueDepthComm(action, id))


if __name__ == '__main__':
    # sns_arn = "arn:aws-cn:sns:cn-northwest-1:182411574528:test"
    sns_arn = "arn:aws-cn:sns:cn-northwest-1:182411574528:Alarm"
    cli = Contants['AWSCLI']
    for i in Contants['AWSREGION']:
        Contants['AWSCLI'] = cli + ' --region ' + i
        add_alert(getAll(), sns_arn)