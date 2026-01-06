## MKM: moran, kagiroi and mungyeong, a set of CJK rime input schemas
本配置包含三個方案：「魔然」,「カギロイ」和「문경」，並在 recipe 中實現了如下連攜:
- 在「魔然」中，使用 `ok` `om` 喚起另外兩種方案的臨時輸入
- 在「カギロイ」和「문경」 中，使用 `C/J/K+後續編碼` 喚起反查功能
### Installation
```sh
bash rime-install rimeinn/rime-mkm/mkm-packages.conf
```
### Customization
通過環境變量可以指定具體分支（moran 默認 trad， 其他默認 main）：

- branch_moran
- branch_kagiroi
- branch_mungyeong
#### Usage Example:

```sh 使用簡體版魔然
branch_moran=simp bash rime-install rimeinn/rime-mkm/mkm-packages.conf
```
