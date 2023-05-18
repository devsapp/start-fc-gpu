import {
  Input,
  Row,
  Col,
  Button,
  Card,
  message,
  notification,
  Space,
  InputNumber,
} from 'antd';
import React from 'react';
import { getEndpoint } from '@/utils/api';
import { ColdStartLoading } from './ColdStartLoading';

async function chat(
  history: { user: boolean; content: string }[],
  historyLength: number,
) {
  const resp = await fetch(`${await getEndpoint()}/chat`, {
    method: 'post',
    body: JSON.stringify(
      history.slice(
        Math.max(0, history.length - historyLength),
        history.length,
      ),
    ),
  });
  const data = await resp.json();
  return data?.text;
}

export function Chat() {
  const [value, setValue] = React.useState('');
  const [loading, setLoading] = React.useState(false);
  const [historyLength, setHistoryLength] = React.useState(1);

  const [history, setHistory] = React.useState<
    {
      user: boolean;
      content: string;
    }[]
  >([]);

  const onSubmit = React.useCallback(() => {
    if (!!value) {
      setLoading(true);
      const newHistory = [...history, { user: true, content: value }];
      setHistory(newHistory);
      setValue('');

      console.log(newHistory);
      chat(newHistory, historyLength)
        .then((result) => {
          setHistory([...newHistory, { user: false, content: result }]);
        })
        .catch((err) => {
          console.error(err);
          message.error('查询失败');
        })
        .finally(() => {
          setLoading(false);
        });
    }
  }, [value, setLoading, setHistory, setValue, history, historyLength]);

  React.useEffect(() => {
    window.scrollTo(0, document.body.scrollHeight);
  }, [history]);

  return (
    <ColdStartLoading
      prewarm={async () => {
        let resp = '';
        try {
          resp = await chat([], 1);
        } catch {}

        if (!resp)
          notification.error({ message: '模型预热失败，请刷新页面重试' });
      }}
    >
      <div style={{ width: '80%', margin: 'auto', marginBottom: 350 }}>
        {history.map((item, idx) => {
          return item.user ? (
            <div key={idx} style={{ width: '100%', margin: '0.5em' }}>
              <b>用户</b>: {item.content}
            </div>
          ) : (
            <Card key={idx} style={{ margin: '2em 0' }}>
              <div style={{ marginBottom: '1em' }}>
                <b>小元</b>
              </div>

              {item.content}
            </Card>
          );
        })}
      </div>

      <Card
        style={{
          position: 'fixed',
          bottom: 0,
          left: 0,
          right: 0,
          boxShadow: '0px -3px 12px #55555555',
        }}
      >
        <Row gutter={8} align="middle">
          <Col flex="auto">
            <Input
              value={value}
              onChange={(e) => setValue(e?.target?.value || '')}
              prefix={<b style={{ marginRight: '1em' }}>用户：</b>}
              suffix={
                <Button type="primary" loading={loading} onClick={onSubmit}>
                  发送
                </Button>
              }
              onKeyDown={(event) => {
                if (event.key === 'Enter' && !!value) {
                  onSubmit();
                }
              }}
              placeholder="请输入问题，在结尾正确使用标点符号可以提升回复质量。"
            />
          </Col>

          <Col>上下文记忆长度</Col>

          <Col>
            <InputNumber
              value={historyLength}
              onChange={(v) => typeof v === 'number' && setHistoryLength(v)}
              min={1}
              max={100}
            />
          </Col>
        </Row>

        <div style={{ marginTop: 24 }}>
          <b>常见问题</b>
        </div>

        <div style={{ marginTop: 8, overflow: 'auto', padding: 12 }}>
          <div style={{ width: 'max-content', margin: 12 }}>
            <Space>
              {[
                '地球有几个大洲？',
                '地球的直径是多少？',
                '你知道什么是驼峰命名法吗？',
                '你更喜欢什么动物？',
                '写一个文章，题目是未来城市。',
                '从南京到上海的路线。',
              ].map((item) => (
                <Card key={item} hoverable onClick={() => setValue(item)}>
                  {item}
                </Card>
              ))}
            </Space>
          </div>
        </div>
      </Card>
    </ColdStartLoading>
  );
}
