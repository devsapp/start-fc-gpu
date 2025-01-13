package controller

import (
	"errors"
	"fmt"
	"net/http"
	"net/url"
	"os"
	"strconv"
	"time"
)

// GetEnvs ...
func GetEnvs() (string, string, string, int, error) {
	watchNamespace := os.Getenv("WATCH_NAMESPACE")
	if watchNamespace == "" {
		return "", "", "", 0, errors.New("WATCH_NAMESPACE 环境变量未设置或者为空")
	}

	fcHookUrl := os.Getenv("FC_HOOK_URL")
	if fcHookUrl == "" {
		return watchNamespace, "", "", 0, errors.New("FC_HOOK_URL 环境变量未设置或者为空")
	}

	fcHookHost := os.Getenv("FC_HOOK_HOST")
	if fcHookHost == "" {
		return watchNamespace, fcHookUrl, "", 0, errors.New("FC_HOOK_HOST 环境变量未设置或者为空")
	}

	podPortStr := os.Getenv("POD_PORT")
	if podPortStr == "" {
		return watchNamespace, fcHookUrl, fcHookHost, 0, errors.New("POD_PORT 环境变量未设置或者为空")
	}
	podPort, err := strconv.Atoi(podPortStr)
	if err != nil {
		return watchNamespace, fcHookUrl, fcHookHost, 0, errors.New("POD_PORT 环境变量的值不是int类型")
	}

	return watchNamespace, fcHookUrl, fcHookHost, podPort, nil
}

// PodUpdateCallback ...
func PodUpdateCallback(fcHookUrl, fcHookHost, podIP, eventType string) {
	// 构建请求体
	payload := RequestPayload{
		PodIP:     podIP,
		EventType: eventType,
	}

	// 执行请求
	err := doRequestWithRetry("GET", fcHookUrl, fcHookHost, payload)
	if err != nil {
		fmt.Printf("HTTP 请求失败: %v\n", err)
		return
	} else {
		fmt.Printf("do PodUpdateCallback successfully with podIP: %s and eventType %s.\n", podIP, eventType)
	}
}

// RequestPayload 定义请求的JSON结构
type RequestPayload struct {
	PodIP     string `json:"PodIP"`
	EventType string `json:"EventType"`
}

// doRequestWithRetry 执行带有退避重试的HTTP请求
func doRequestWithRetry(method, url, host string, payload RequestPayload) error {
	var lastErr error
	initialDelay := 1 * time.Second
	maxRetries := 10
	maxDelay := 10 * time.Second

	delay := initialDelay

	urlRemovePath, err := removePath(url)
	if err != nil {
		return fmt.Errorf("解析URL时出错: %w", err)
	}

	// 构建带有查询参数的URL
	urlWithParams, err := addQueryParams(urlRemovePath, payload)
	if err != nil {
		return fmt.Errorf("构建URL时出错: %w", err)
	}
	fmt.Printf("urlWithParams is %s\n", urlWithParams)

	for attempt := 1; attempt <= maxRetries; attempt++ {
		resp, err := makeRequest(method, urlWithParams, host)
		if err == nil {
			defer resp.Body.Close()
			// 成功，解析响应
			if resp.StatusCode >= 200 && resp.StatusCode < 300 {
				return nil
			} else if resp.StatusCode >= 500 {
				// 5xx状态码，重试
				lastErr = errors.New("server error")
			} else {
				// 非2xx/5xx状态码，视为错误，但不重试
				return fmt.Errorf("received non-2xx status code: %d", resp.StatusCode)
			}
		} else {
			lastErr = err
		}

		// 检查是否需要重试
		if attempt < maxRetries {
			fmt.Printf("Attempt %d failed: %v. Retrying in %v...\n", attempt, lastErr, delay)
			time.Sleep(delay)
			// 指数退避，延迟时间加倍但不超过最大延迟
			delay = delay * 2
			if delay > maxDelay {
				delay = maxDelay
			}
		}
	}

	return fmt.Errorf("all %d attempts failed: last error: %w", maxRetries, lastErr)
}

func removePath(originalURL string) (string, error) {
	// 解析原始 URL
	parsedURL, err := url.Parse(originalURL)
	if err != nil {
		return "", err
	}

	// 清空与路径相关的字段
	parsedURL.Path = ""
	parsedURL.RawPath = ""
	parsedURL.RawQuery = ""
	parsedURL.Fragment = ""
	parsedURL.Opaque = ""

	// 返回修改后的 URL 字符串
	return parsedURL.String(), nil
}

// addQueryParams 构建带有查询参数的URL
func addQueryParams(baseURL string, payload RequestPayload) (string, error) {
	if payload.EventType == "Add" {
		baseURL = baseURL + "/endpoint/register"
	} else if payload.EventType == "Delete" {
		baseURL = baseURL + "/endpoint/unregister"
	} else {
		return "", fmt.Errorf("wrong payload evenType: %s", payload.EventType)
	}

	u, err := url.Parse(baseURL)
	if err != nil {
		return "", err
	}

	q := u.Query()
	q.Set("endpoint", payload.PodIP)
	u.RawQuery = q.Encode()

	return u.String(), nil
}

// makeRequest 构建并发送HTTP请求
func makeRequest(method, url, host string) (*http.Response, error) {
	client := &http.Client{
		Timeout: 100 * time.Second, // 设置超时时间
	}

	req, err := http.NewRequest(method, url, nil)
	if err != nil {
		return nil, fmt.Errorf("error creating request: %w", err)
	}

	// 设置自定义Host Header
	req.Host = host

	// 发送请求
	resp, err := client.Do(req)
	if err != nil {
		return nil, fmt.Errorf("error making request: %w", err)
	}

	return resp, nil
}
