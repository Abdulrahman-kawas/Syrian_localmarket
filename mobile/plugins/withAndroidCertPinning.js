// Expo config plugin: Android certificate pinning.
//
// Writes an Android network-security-config with an SPKI pin-set and points the
// app's manifest at it. Takes effect in release / dev-client builds (not Expo
// Go). Configure the host + pins in app.config.ts; see docs/CERT_PINNING.md.

const { withAndroidManifest, withDangerousMod, AndroidConfig } = require('@expo/config-plugins');
const fs = require('fs');
const path = require('path');

const DEFAULT_HOST = 'api.localmarket.app';
const DEFAULT_PINS = ['REPLACE_WITH_REAL_SPKI_PIN_BASE64='];

function buildXml(host, pins) {
  const pinLines = pins.map((p) => `      <pin digest="SHA-256">${p}</pin>`).join('\n');
  return (
    '<?xml version="1.0" encoding="utf-8"?>\n' +
    '<network-security-config>\n' +
    '  <domain-config>\n' +
    `    <domain includeSubdomains="true">${host}</domain>\n` +
    '    <pin-set>\n' +
    `${pinLines}\n` +
    '    </pin-set>\n' +
    '  </domain-config>\n' +
    '</network-security-config>\n'
  );
}

function withNetworkSecurityFile(config, host, pins) {
  return withDangerousMod(config, [
    'android',
    async (cfg) => {
      const xmlDir = path.join(
        cfg.modRequest.platformProjectRoot,
        'app/src/main/res/xml',
      );
      fs.mkdirSync(xmlDir, { recursive: true });
      fs.writeFileSync(
        path.join(xmlDir, 'network_security_config.xml'),
        buildXml(host, pins),
      );
      return cfg;
    },
  ]);
}

function withManifestReference(config) {
  return withAndroidManifest(config, (cfg) => {
    const app = AndroidConfig.Manifest.getMainApplicationOrThrow(cfg.modResults);
    app.$['android:networkSecurityConfig'] = '@xml/network_security_config';
    return cfg;
  });
}

module.exports = function withAndroidCertPinning(config, props = {}) {
  const host = props.host || DEFAULT_HOST;
  const pins = props.pins && props.pins.length ? props.pins : DEFAULT_PINS;
  config = withNetworkSecurityFile(config, host, pins);
  config = withManifestReference(config);
  return config;
};
