import { ColdStartLoading } from '@/components/ColdStartLoading';
import { ResultList } from '@/components/List';
import { UploadImage } from '@/components/Upload';
import { getEndpoint } from '@/utils/api';
import { getBase64Src } from '@/utils/blob';
import { md5 } from '@/utils/md5';
import { ImageItem } from '@/utils/type';
import { Alert, Card, Space, Typography, notification } from 'antd';
import React from 'react';

async function getURLResult(url: string) {
  const resp = await fetch(
    `${await getEndpoint()}/url?url=${encodeURIComponent(url)}`,
  );
  const data = await resp.json();
  return data?.data?.caption;
}

async function getBase64Result(b64: string) {
  const resp = await fetch(`${await getEndpoint()}/base64`, {
    method: 'POST',
    body: b64,
  });
  const data = await resp.json();
  return data?.data?.caption;
}

export default function HomePage() {
  const [images, setImages] = React.useState<ImageItem[]>([]);
  const [resultMap, setResultMap] = React.useState<{
    [hash: string]: string | false | undefined;
  }>({});

  const getResult = React.useCallback(
    async (img: ImageItem) => {
      setResultMap((prev) => ({ ...prev, [img.hash]: undefined }));
      let retry = 5;
      let isOk = false;

      const req = async () => {
        try {
          const result = await (img.isURL
            ? getURLResult(img.url)
            : getBase64Result(img?.data || ''));
          setResultMap((prev) => ({ ...prev, [img.hash]: result }));
          isOk = true;
        } catch {
          setResultMap((prev) => ({ ...prev, [img.hash]: false }));
        }
      };

      // 在未完成时，重试 5 次
      while (retry-- && !isOk) {
        await req();

        // 请求不要太频繁，间隔 1s
        if (!isOk) await new Promise((resolve) => setTimeout(resolve, 1000));
        else break;
      }

      return isOk;
    },
    [setResultMap],
  );

  return (
    <ColdStartLoading
      prewarm={async () => {
        const isOk = await getResult({
          hash: 'prewarm',
          url: 'https://alice-open.oss-cn-zhangjiakou.aliyuncs.com/mPLUG/image_captioning.png',
          isURL: true,
        });

        if (!isOk)
          notification.error({ message: '模型预热失败，请刷新页面重试' });
      }}
    >
      <Space direction="vertical" size="large" style={{ width: '100%' }}>
        <Card>
          <Typography.Title>mPLUG图像描述模型-中文-base</Typography.Title>
          <Typography.Text>
            图像描述：给定一张图片，模型根据图片信息生成一句对应描述。可以应用于给一张图片配上一句文字或者打个标签的场景。注：本模型为mPLUG-图像描述的中文Base模型，参数量约为3.5亿。
          </Typography.Text>
          <Typography.Link href="https://www.modelscope.cn/models/damo/mplug_image-captioning_coco_base_zh/summary" target="_blank">
            模型链接
          </Typography.Link>

          <Typography.Link
            href="https://modelscope.cn/models/damo/mplug_image-captioning_coco_base_zh/summary"
            style={{ marginLeft: '2em' }}
            target="_blank"
          >
            Apache License 2.0
          </Typography.Link>
        </Card>

        <Alert
          message="首次调用或长时间未交互时需要进行模型加载，请耐心等待"
          type="info"
          style={{ color: '#4baef4' }}
        />

        <Space
          direction="vertical"
          size="large"
          style={{ width: '90%', padding: '0 5%' }}
        >
          <UploadImage
            urlCallback={(url) => {
              const item = {
                url,
                hash: md5(url),
                isURL: true,
              };
              setImages([...images, item]);

              getResult(item);
            }}
            uploadCallback={(b64) => {
              const item = {
                data: b64,
                url: getBase64Src(b64),
                hash: md5(b64),
                isURL: false,
              };
              setImages([...images, item]);

              getResult(item);
            }}
          />
          <ResultList images={images} resultMap={resultMap} retry={getResult} />
        </Space>
      </Space>
    </ColdStartLoading>
  );
}
