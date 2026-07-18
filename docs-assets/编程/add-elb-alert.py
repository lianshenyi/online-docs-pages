#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
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



# TargetResponseTime,15分钟检查3次，当返回响应时间平均大于或等于5s，就告警。
def getTargetResponseTimeComm(elb_name, elb_arn, sns_arn):
    mertic = 'TargetResponseTime'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "ALB_{name}_{mertic} >= 5s" \
--alarm-description "aws alb {mertic}" \
--metric-name {mertic} \
--namespace AWS/ApplicationELB \
--statistic Average \
--period 300 \
--threshold 5 \
--comparison-operator GreaterThanOrEqualToThreshold \
--treat-missing-data notBreaching \
--evaluation-periods 1 \
--datapoints-to-alarm 1 \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions \"Name=LoadBalancer,Value=app/{elb_arn}"'''.format(
        cli=Contants['AWSCLI'], name=elb_name, action=sns_arn, elb_arn=elb_arn, mertic=mertic)


# NewFlowCount 15分钟检查3次，平均值大于或等于 20000，就告警。
def getNewFlowCountComm(elb_name, elb_arn, sns_arn):
    mertic = 'NewFlowCount'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "NLB_{name}_{mertic} > 20000" \
--alarm-description "aws elb {mertic}" \
--metric-name {mertic} \
--namespace AWS/NetworkELB \
--statistic Sum \
--period 300 \
--threshold 20000 \
--comparison-operator GreaterThanOrEqualToThreshold \
--treat-missing-data notBreaching \
--evaluation-periods 3 \
--datapoints-to-alarm 3 \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions \"Name=LoadBalancer,Value=net/{elb_arn}"'''.format(
        cli=Contants['AWSCLI'], name=elb_name, action=sns_arn, elb_arn=elb_arn, mertic=mertic)


# ALB-RequestCount 15分钟检查3次，平均值大于或等于 20000，就告警。
def getAlbRequestCountComm(elb_name, elb_arn, sns_arn):
    mertic = 'RequestCount'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "ALB_{name}_{mertic} > 20000" \
--alarm-description "aws elb {mertic}" \
--metric-name {mertic} \
--namespace AWS/ApplicationELB \
--statistic Sum \
--period 300 \
--threshold 20000 \
--comparison-operator GreaterThanOrEqualToThreshold \
--treat-missing-data notBreaching \
--evaluation-periods 3 \
--datapoints-to-alarm 3 \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions \"Name=LoadBalancer,Value=app/{elb_arn}"'''.format(
        cli=Contants['AWSCLI'], name=elb_name, action=sns_arn, elb_arn=elb_arn, mertic=mertic)

# HTTPCode_Target_5XX_Count 一分钟采集一次，周期为1分钟，1个数据点中有1次超过阈值就告警，当5xx超过10个为超过阈值
def getHTTPCode_Target_5XX_CountComm(elb_name, elb_arn, sns_arn):
    mertic = 'HTTPCode_Target_5XX_Count'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "ALB_{name}_{mertic} >= 10" \
--alarm-description "aws alb {mertic}" \
--metric-name {mertic} \
--namespace AWS/ApplicationELB \
--statistic Sum \
--period 300 \
--threshold 10 \
--comparison-operator GreaterThanOrEqualToThreshold \
--treat-missing-data notBreaching \
--evaluation-periods 1 \
--datapoints-to-alarm 1 \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions \"Name=LoadBalancer,Value=app/{elb_arn}"'''.format(
        cli=Contants['AWSCLI'], name=elb_name, action=sns_arn, elb_arn=elb_arn, mertic=mertic)

# HTTP_4XX 一分钟采集一次，周期为5分钟，5个数据点中有三次超过阈值就告警，当4xx超过10%为超过阈值
def getHTTPCode_Target_4XX_CountComm(elb_name, elb_arn, sns_arn):
    mertic = 'HTTPCode_Target_4XX_Count'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "ALB_{name}_{mertic} >= 50" \
--alarm-description "aws alb {mertic}" \
--metric-name {mertic} \
--namespace AWS/ApplicationELB \
--statistic Sum \
--period 300 \
--threshold 50 \
--comparison-operator GreaterThanOrEqualToThreshold \
--treat-missing-data notBreaching \
--evaluation-periods 1 \
--datapoints-to-alarm 1 \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions \"Name=LoadBalancer,Value=app/{elb_arn}"'''.format(
        cli=Contants['AWSCLI'], name=elb_name, action=sns_arn, elb_arn=elb_arn, mertic=mertic)

# ClientTLSNegotiationErrorCount 15周期为5分钟，5个数据点中有三次超过阈值就告警
def getClientTLSNegotiationErrorCountComm(elb_name, elb_arn, sns_arn):
    mertic = 'HTTPCode_Target_4XX_Count'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "ALB_{name}_{mertic} > 100" \
--alarm-description "aws elb {mertic}" \
--metric-name {mertic} \
--namespace AWS/ApplicationELB \
--statistic Sum \
--period 300 \
--threshold 100 \
--comparison-operator GreaterThanOrEqualToThreshold \
--treat-missing-data notBreaching \
--evaluation-periods 3 \
--datapoints-to-alarm 3 \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions \"Name=LoadBalancer,Value=app/{elb_arn}"'''.format(
        cli=Contants['AWSCLI'], name=elb_name, action=sns_arn, elb_arn=elb_arn, mertic=mertic)

# ClientTLSNegotiationErrorCount 15周期为5分钟，5个数据点中有三次超过阈值就告警
def getUnHealthyHostCountComm(elb_name, elb_arn, sns_arn):
    mertic = 'UnHealthyHostCount'
    print("#####开始配置 %s#####" % mertic)
    return '''{cli} cloudwatch put-metric-alarm \
--alarm-name "NLB_{name}_{mertic} >= 1" \
--alarm-description "aws nlb {mertic}" \
--metric-name {mertic} \
--namespace AWS/NetworkELB \
--statistic Sum \
--period 300 \
--threshold 1 \
--comparison-operator GreaterThanOrEqualToThreshold \
--treat-missing-data notBreaching \
--evaluation-periods 1 \
--datapoints-to-alarm 1 \
--alarm-actions "{action}" \
--ok-actions "{action}" \
--dimensions \"Name=LoadBalancer,Value=net/{elb_arn}"'''.format(
        cli=Contants['AWSCLI'], name=elb_name, action=sns_arn, elb_arn=elb_arn, mertic=mertic)



# AWS/ApplicationELB
# ClientTLSNegotiationErrorCount
# LoadBalancer: app/go-api-server/6a36c84e3b1bf5ce

# 执行命令函数
def execCommand(comm):
    try:
        print(comm)
        (status, stdout) = subprocess.getstatusoutput(comm)
        print(status)
        return stdout
    except Exception as e:
        print(e)


# 获取当前可用区内所有elb2的信息
def getAll():
    comm1 = "%s elbv2 describe-load-balancers" % Contants['AWSCLI']
    AllLb2Details = json.loads(execCommand(comm1))['LoadBalancers']
    arndict = CreateDict()
    for i in range(0, len(AllLb2Details)):
        lbarn = AllLb2Details[i]["LoadBalancerArn"]
        lbname = AllLb2Details[i]["LoadBalancerName"]
        arndict[lbname]["type"] = AllLb2Details[i]["Type"]
        arndict[lbname]["lbarn"] = lbarn
    return arndict


# 添加报警
def add_alert(arn_data, sns_arn):
    for elb_name, elb_value in arn_data.items():
        if elb_value['type'] == 'application':
            elb_arn = re.split(r'loadbalancer/app/', elb_value['lbarn'])[-1]
            # execCommand(getAlbRequestCountComm(elb_name, elb_arn, sns_arn))
            # execCommand(getTargetResponseTimeComm(elb_name, elb_arn, sns_arn))
            # execCommand(getHTTPCode_Target_5XX_CountComm(elb_name, elb_arn, sns_arn))
            execCommand(getHTTPCode_Target_4XX_CountComm(elb_name, elb_arn, sns_arn))
            # execCommand(getClientTLSNegotiationErrorCountComm(elb_name, elb_arn, sns_arn))
        if elb_value['type'] == 'network':
            elb_arn = re.split(r'loadbalancer/net/', elb_value['lbarn'])[-1]
            # execCommand(getUnHealthyHostCountComm(elb_name, elb_arn, sns_arn))
        #     print("app")
        #     elb_arn = re.split(r'loadbalancer/app/', elb_value['lbarn'])[-1]
        # elif elb_value['type'] == 'network':
        #     print("net")
        #     elb_arn = re.split(r'loadbalancer/net/', elb_value['lbarn'])[-1]
        # print(elb_arn)
        # for port, taggroup in elb_value['lbgroup'].items():
        #     print("######################################################")
        #     taggroup = re.split(r':targetgroup/', taggroup)[-1]
            # execCommand(getHealthyHostCountComm(elb_name, port, taggroup, elb_arn, sns_arn))
            # execCommand(getRequestCountComm(elb_name, port, elb_arn, sns_arn))
            
            # execCommand(getUnHealthyHostCountComm(elb_name, port, taggroup, elb_arn, sns_arn))
            # execCommand(getActiveFlowCountComm(elb_name, port, taggroup, elb_arn, sns_arn))
            # execCommand(getProcessedBytesComm(elb_name, port, taggroup, elb_arn, sns_arn))

        # if elb_value['type'] != 'network':
        #     execCommand(getHTTPCode_Target_5XX_CountComm(elb_name, port, taggroup, elb_arn, sns_arn))
        #     execCommand(getHTTPCode_Target_4XX_CountComm(elb_name, port, taggroup, elb_arn, sns_arn))

if __name__ == '__main__':
    # sns_arn = "arn:aws-cn:sns:cn-northwest-1:182411574528:test"
    sns_arn = "arn:aws-cn:sns:cn-northwest-1:182411574528:Alarm"

    cli = Contants['AWSCLI']
    for i in Contants['AWSREGION']:
        Contants['AWSCLI'] = cli + ' --region ' + i
        add_alert(getAll(), sns_arn)
