import { blobToBase64 } from '@/utils/blob';
import { Button, Col, Image, Input, Row, Space, Upload, message } from 'antd';
import React from 'react';
const { Dragger } = Upload;

function noUploadDialog(e: React.MouseEvent<any, MouseEvent>) {
  e.preventDefault();
  e.stopPropagation();
}
export function UploadImage(props: {
  urlCallback: (url: string) => void;
  uploadCallback: (base64: string) => void;
}) {
  const { urlCallback, uploadCallback } = props;
  const [url, setURL] = React.useState(
    'https://alice-open.oss-cn-zhangjiakou.aliyuncs.com/mPLUG/image_captioning.png',
  );

  return (
    <Dragger
      accept="image/*"
      showUploadList={false}
      beforeUpload={async (file) => {
        const isImg = file.type.startsWith('image/');

        if (!isImg) {
          console.log(file.type);
          message.error(`${file.name}(${file.type}) 不是允许的图片格式`);
          return Upload.LIST_IGNORE;
        }

        const b64 = await blobToBase64(file);
        uploadCallback(b64);
      }}
    >
      <Space direction="vertical" style={{ width: '100%' }}>
        <span>输入图片地址或上传一张图片（支持拖拽）</span>

        {url && (
          <div style={{ display: 'inline' }} onClick={noUploadDialog}>
            <Image src={url} style={{ maxWidth: 200, maxHeight: 200 }} />
          </div>
        )}
        <Row gutter={8} style={{ margin: 32 }}>
          <Col flex="auto" onClick={noUploadDialog}>
            <Input
              value={url}
              onChange={(e) => setURL(e?.target?.value || '')}
              allowClear
            />
          </Col>
          <Col>
            {url ? (
              <Button
                type="primary"
                onClick={(e) => {
                  noUploadDialog(e);

                  urlCallback(url);
                  setURL('');
                }}
              >
                使用图片链接
              </Button>
            ) : (
              <Button>选择图片</Button>
            )}
          </Col>
        </Row>
      </Space>
    </Dragger>
  );
}
