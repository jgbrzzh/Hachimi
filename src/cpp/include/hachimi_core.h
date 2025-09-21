#ifndef HACHIMI_CORE_H
#define HACHIMI_CORE_H

#include <string>
#include <vector>

namespace hachimi {

/**
 * 哈吉咪加密解密核心类
 * 实现基于XOR和置换的简单而有效的加密算法
 */
class HachimiCore {
public:
    /**
     * 构造函数
     */
    HachimiCore();
    
    /**
     * 析构函数
     */
    ~HachimiCore();

    /**
     * 加密字符串
     * @param plaintext 明文字符串
     * @param key 加密密钥
     * @return 加密后的字节数组
     */
    std::vector<uint8_t> encrypt(const std::string& plaintext, const std::string& key);

    /**
     * 解密字节数组
     * @param ciphertext 加密的字节数组
     * @param key 解密密钥
     * @return 解密后的字符串
     */
    std::string decrypt(const std::vector<uint8_t>& ciphertext, const std::string& key);

    /**
     * 加密文件
     * @param input_path 输入文件路径
     * @param output_path 输出文件路径
     * @param key 加密密钥
     * @return 是否成功
     */
    bool encrypt_file(const std::string& input_path, const std::string& output_path, const std::string& key);

    /**
     * 解密文件
     * @param input_path 加密文件路径
     * @param output_path 输出文件路径
     * @param key 解密密钥
     * @return 是否成功
     */
    bool decrypt_file(const std::string& input_path, const std::string& output_path, const std::string& key);

private:
    /**
     * 生成密钥流
     * @param key 原始密钥
     * @param length 需要的密钥流长度
     * @return 密钥流
     */
    std::vector<uint8_t> generate_key_stream(const std::string& key, size_t length);

    /**
     * 哈吉咪置换函数
     * @param data 输入数据
     * @param key_stream 密钥流
     */
    void hachimi_transform(std::vector<uint8_t>& data, const std::vector<uint8_t>& key_stream);

    /**
     * 哈吉咪逆置换函数
     * @param data 输入数据
     * @param key_stream 密钥流
     */
    void hachimi_inverse_transform(std::vector<uint8_t>& data, const std::vector<uint8_t>& key_stream);

    // 内部状态
    std::vector<uint8_t> salt_;
    static const size_t SALT_SIZE = 16;
    static const uint8_t HACHIMI_MAGIC = 0x48; // 'H' for Hachimi
};

} // namespace hachimi

#endif // HACHIMI_CORE_H