---
layout: default
title: Privacy Policy
permalink: /privacy-en/
---

# Privacy Policy

**App Name: SheetWidget (the "App")**
**Effective Date: June 21, 2026 / Last Updated: June 21, 2026**


---

`SheetWidget` ("we", "us", or "our") provides this Privacy Policy (the "Policy") describing how the App handles your personal information and user data. By using the App, you agree to this Policy.

## 1. Core Principle

The App does **not transmit or store your data on any external server**. We do not operate a backend server. All data processing occurs either on your device or directly between your own Google account and Google's services.

## 2. Information We Handle

The App handles the following information only to the extent necessary to provide its features.

### (1) Google Account Information
- Your Google account email address and profile information
- OAuth authentication tokens (access token and refresh token)

### (2) Spreadsheet Information
- Configuration data such as the Google Spreadsheet identifier, sheet name, and cell range you select
- Cell values and formatting information retrieved from the spreadsheet for display

### (3) Purchase Information
- Your in-app purchase status (one-time purchases and subscriptions). All payments are processed through Apple (the App Store). We do not collect or store payment details such as credit card numbers.

### (4) Advertising Information (if advertising is enabled)
- For ad delivery, third-party advertising providers may collect advertising identifiers (IDFA), device information, approximate location, etc. (see "8. Advertising").

## 3. Purposes of Use

We use the information solely for the following purposes:
1. To retrieve and display Google Spreadsheet data in widgets, etc.
2. To save and restore your widget configurations
3. To refresh tokens using the refresh token when the access token expires
4. To provide and unlock features via in-app purchases
5. To display advertisements (if advertising is enabled)

## 4. Where and How Data Is Stored

| Data | Storage Location | Notes |
|---|---|---|
| Access / Refresh tokens | Keychain and App Group shared container on the device | Never sent off-device |
| Spreadsheet config & display data | App Group shared container on the device | Same as above |
| Purchase status | On the device | Based on Apple purchase information |

The App never sends this data to any server operated by us. Spreadsheet data is requested directly from Google's servers over HTTPS using your token.

## 5. Disclosure to Third Parties

Except as required by law, we do not provide or sell your information to third parties. For its functionality, the App communicates with the following third-party services:

- **Google LLC**: Authentication (Google Sign-In) and retrieval of spreadsheet data (Google Sheets API)
- **Apple Inc.**: Processing of in-app purchases
- **Advertising providers** (if advertising is enabled): Ad delivery

## 6. Handling of Google User Data (Google API Services User Data Policy)

The App's use and transfer of information received from Google APIs adhere to the [Google API Services User Data Policy](https://developers.google.com/terms/api-services-user-data-policy), including the Limited Use requirements.

- Scopes requested by the App:
  - `https://www.googleapis.com/auth/spreadsheets.readonly` (read spreadsheets)
- You specify a spreadsheet by pasting its share link (URL). The App does not list or browse files in your Google Drive.
- Spreadsheet data is used **solely to provide the App's core feature of displaying it to you**.
- We never use such data for advertising purposes, nor sell or transfer it to third parties.
- We do not allow humans to read such data, except (a) with your explicit consent, (b) for security purposes, (c) to comply with applicable law, or (d) as otherwise permitted by the policy.

## 7. Data Retention and Deletion

- Signing out within the App deletes the authentication tokens stored on your device.
- **Uninstalling** the App from your device deletes all App-related data stored on the device (settings, cache, tokens).
- You may revoke the App's access at any time from your [Google Account security settings](https://myaccount.google.com/permissions).

## 8. Advertising (if advertising is enabled)

The App may, in the future, display third-party advertisements (e.g., Google AdMob). Advertising providers may use advertising identifiers to deliver relevant ads. You can manage ad personalization from your device under "Settings > Privacy & Security > Tracking", etc. Please refer to each provider's privacy policy for details.

> Note: While advertising features are not implemented or enabled, no advertising-related data collection described in this section occurs.

## 9. Children's Privacy

The App is not directed to children under the age of 13. We do not knowingly collect personal information from children under 13.

## 10. Security

Authentication tokens are stored on the device using OS-provided protection mechanisms such as the iOS Keychain. However, no method of transmission over the Internet or electronic storage is completely secure, and we cannot guarantee absolute security.

## 11. International Data Transfers

Because the App uses Google's services, data may be processed on Google's servers in various countries. Such processing is governed by Google's privacy policy.

## 12. Changes to This Policy

We may revise this Policy as necessary. For material changes, we will provide notice within the App or on a public page. Your continued use of the App after such changes constitutes acceptance of the revised Policy.

## 13. Contact

For inquiries regarding this Policy, please contact:

- Operator: `SheetWidget`
- Contact: `sheetwidget@gmail.com`
- Support: `sheetwidget@gmail.com`

---

This Policy is governed by `the laws of Japan (the Tokyo District Court as the court of first instance)`.
