import { ImageItem } from '@/utils/type';
import { LoadingOutlined } from '@ant-design/icons';
import { Avatar, Button, Image, List, Switch } from 'antd';
import React from 'react';

export function ResultList(props: {
  images: ImageItem[];
  resultMap: { [hash: string]: string | false | undefined };
  retry: (img: ImageItem) => void;
}) {
  const { images, resultMap, retry } = props;
  const [replaceSpace, setReplaceSpace] = React.useState(true);

  return (
    <List
      dataSource={images}
      header={
        <div style={{ width: '100%', textAlign: 'right' }}>
          <Switch
            checked={replaceSpace}
            onChange={setReplaceSpace}
            checkedChildren="去除空格"
            unCheckedChildren="保留空格"
          />
        </div>
      }
      renderItem={(item) => {
        const result = resultMap[item.hash];
        return (
          <List.Item key={item.hash}>
            <List.Item.Meta
              avatar={
                <Image
                  width={100}
                  height={100}
                  placeholder={
                    <Avatar
                      shape="square"
                      src={item.url}
                      size={100}
                      style={{ cursor: 'pointer' }}
                    />
                  }
                  preview={{
                    src: item.url,
                  }}
                />
              }
              description={
                result === false ? (
                  <div>
                    解析错误，是否
                    <Button
                      type="link"
                      onClick={() => retry(item)}
                      style={{ padding: 0 }}
                    >
                      重试
                    </Button>
                    ?
                  </div>
                ) : !!result ? (
                  replaceSpace ? (
                    result?.replace(/ /g, '')
                  ) : (
                    result
                  )
                ) : (
                  <div>
                    <LoadingOutlined /> 正在解析中，请稍等片刻...
                  </div>
                )
              }
            />
          </List.Item>
        );
      }}
    />
  );
}
