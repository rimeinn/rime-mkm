## MKM: moran, kagiroi and mungyeong, a set of CJK rime input schemas
本配置包含三個方案：「魔然」、「カギロイ」和「문경」，並在 recipe 中實現了如下連攜:
- 在「魔然」中，使用 `ok` `om` 喚起另外兩種方案的臨時輸入
- 在「カギロイ」和「문경」 中，使用 `C/J/K+後續編碼` 喚起反查功能
- 在「カギロイ」和「문경」 中，通過 `` ` `` 調用「魔然」中的自然碼輔碼，實現間接輔助篩選

### Installation
需要預先安裝 [plum](https://github.com/rime/plum)，獲取 rime-install 工具

```sh
bash rime-install rimeinn/rime-mkm/mkm-packages.conf
```

或者在 [Release Page](https://github.com/rimeinn/rime-mkm/releases/tag/nightly) 選擇對應的 ZIP 包下載，解壓至 Rime 用戶目錄重新部署即可


### Customization
通過環境變量可以指定具體分支（moran 默認 trad， 其他默認 main）：

- branch_moran
- branch_kagiroi
- branch_mungyeong

#### Usage Example:
使用簡體版魔然：
```sh
branch_moran=simp bash rime-install rimeinn/rime-mkm/mkm-packages.conf
```

### References
- [plum](https://github.com/rime/plum)：Rime 方案配置管理工具
- [魔然](https://github.com/rimeinn/rime-moran)：魔改自然碼輸入方案
- [カギロイ](https://github.com/rimeinn/rime-kagiroi)：日語輸入方案
- [문경](https://github.com/rimeinn/rime-mungyeong)：韓語輸入方案
