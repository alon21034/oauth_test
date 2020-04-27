將部分的功能截圖以供參考，但由於大多功能需要整個操作流程，所以得麻煩你們驗證，或有機會的話留待現場 Demo。

### 1. 用戶註冊功能,支援:
> - Email
> - Google
> - Facebook

參見 `image1.png`

### 2. 用戶成功註冊後,觸發以下功能:
> - 把使用者的名稱及Email存在資料庫
> - 寄送註冊成功 Email
> - 贈送一張優惠卷到該帳戶
> - 回傳 Token ,格式: { token: "xxx"}
 
參見 `image4.png`, `image6.png` 及 `image7.png`

### 3. 使用 Email 註冊發生錯誤
- 回傳 error message,格式: { "error": "error message" }
- 錯誤的情境包括:
> Email 格式錯誤

參見 `image3.png`

- Email 已被註冊
>  密碼少於8個字

參見 `image2.png`

- 確認密碼輸入不正確

#### 我認為確認密碼輸入不正確應在前端做檢查較為合理(`image8.png`)

- #### 多處理了註冊時 username 重複的部分（`image5.png`）

### 4. 使用 Facebook 或 Google 註冊發生錯誤
> 回傳 error message,格式: { "error": "error message" }
> 錯誤的情境包括:
> 前端發送的驗證 authorize_code 無效
> 若用戶已經註冊,則會跳過註冊,直接拿到token