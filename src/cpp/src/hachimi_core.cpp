#include "hachimi_core.h"
#include <fstream>
#include <random>
#include <algorithm>
#include <cstring>

namespace hachimi {

HachimiCore::HachimiCore() {
    // 初始化盐值
    salt_.resize(SALT_SIZE);
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<uint8_t> dis(0, 255);
    
    for (size_t i = 0; i < SALT_SIZE; ++i) {
        salt_[i] = dis(gen);
    }
}

HachimiCore::~HachimiCore() {
    // 清理敏感数据
    std::fill(salt_.begin(), salt_.end(), 0);
}

std::vector<uint8_t> HachimiCore::encrypt(const std::string& plaintext, const std::string& key) {
    if (plaintext.empty() || key.empty()) {
        return std::vector<uint8_t>();
    }

    // 转换字符串为字节数组
    std::vector<uint8_t> data(plaintext.begin(), plaintext.end());
    
    // 生成密钥流
    auto key_stream = generate_key_stream(key, data.size());
    
    // 应用哈吉咪变换
    hachimi_transform(data, key_stream);
    
    // 添加盐值和魔数标识
    std::vector<uint8_t> result;
    result.reserve(1 + SALT_SIZE + data.size());
    
    result.push_back(HACHIMI_MAGIC);
    result.insert(result.end(), salt_.begin(), salt_.end());
    result.insert(result.end(), data.begin(), data.end());
    
    return result;
}

std::string HachimiCore::decrypt(const std::vector<uint8_t>& ciphertext, const std::string& key) {
    if (ciphertext.size() < 1 + SALT_SIZE || key.empty()) {
        return "";
    }
    
    // 验证魔数
    if (ciphertext[0] != HACHIMI_MAGIC) {
        return "";
    }
    
    // 提取盐值
    std::vector<uint8_t> file_salt(ciphertext.begin() + 1, ciphertext.begin() + 1 + SALT_SIZE);
    
    // 提取加密数据
    std::vector<uint8_t> data(ciphertext.begin() + 1 + SALT_SIZE, ciphertext.end());
    
    // 临时设置盐值用于解密
    auto original_salt = salt_;
    salt_ = file_salt;
    
    // 生成密钥流
    auto key_stream = generate_key_stream(key, data.size());
    
    // 应用哈吉咪逆变换
    hachimi_inverse_transform(data, key_stream);
    
    // 恢复原盐值
    salt_ = original_salt;
    
    // 转换为字符串
    return std::string(data.begin(), data.end());
}

bool HachimiCore::encrypt_file(const std::string& input_path, const std::string& output_path, const std::string& key) {
    std::ifstream input(input_path, std::ios::binary);
    if (!input.is_open()) {
        return false;
    }
    
    std::ofstream output(output_path, std::ios::binary);
    if (!output.is_open()) {
        return false;
    }
    
    // 读取整个文件
    std::vector<uint8_t> buffer((std::istreambuf_iterator<char>(input)),
                                std::istreambuf_iterator<char>());
    input.close();
    
    if (buffer.empty()) {
        return false;
    }
    
    // 加密数据
    std::string data_str(buffer.begin(), buffer.end());
    auto encrypted = encrypt(data_str, key);
    
    if (encrypted.empty()) {
        return false;
    }
    
    // 写入加密数据
    output.write(reinterpret_cast<const char*>(encrypted.data()), encrypted.size());
    output.close();
    
    return true;
}

bool HachimiCore::decrypt_file(const std::string& input_path, const std::string& output_path, const std::string& key) {
    std::ifstream input(input_path, std::ios::binary);
    if (!input.is_open()) {
        return false;
    }
    
    std::ofstream output(output_path, std::ios::binary);
    if (!output.is_open()) {
        return false;
    }
    
    // 读取加密文件
    std::vector<uint8_t> buffer((std::istreambuf_iterator<char>(input)),
                                std::istreambuf_iterator<char>());
    input.close();
    
    if (buffer.empty()) {
        return false;
    }
    
    // 解密数据
    auto decrypted = decrypt(buffer, key);
    
    if (decrypted.empty()) {
        return false;
    }
    
    // 写入解密数据
    output.write(decrypted.data(), decrypted.size());
    output.close();
    
    return true;
}

std::vector<uint8_t> HachimiCore::generate_key_stream(const std::string& key, size_t length) {
    std::vector<uint8_t> key_stream;
    key_stream.reserve(length);
    
    // 结合密钥和盐值生成密钥流
    std::string extended_key = key;
    extended_key.insert(extended_key.end(), salt_.begin(), salt_.end());
    
    // 使用简单的伪随机数生成器
    uint32_t seed = 0;
    for (char c : extended_key) {
        seed = seed * 31 + static_cast<uint8_t>(c);
    }
    
    std::mt19937 gen(seed);
    std::uniform_int_distribution<uint8_t> dis(1, 255); // 避免0值
    
    for (size_t i = 0; i < length; ++i) {
        key_stream.push_back(dis(gen));
    }
    
    return key_stream;
}

void HachimiCore::hachimi_transform(std::vector<uint8_t>& data, const std::vector<uint8_t>& key_stream) {
    if (data.size() != key_stream.size()) {
        return;
    }
    
    // 第一轮：XOR操作
    for (size_t i = 0; i < data.size(); ++i) {
        data[i] ^= key_stream[i];
    }
    
    // 第二轮：位移和置换
    for (size_t i = 0; i < data.size(); ++i) {
        uint8_t val = data[i];
        uint8_t key_val = key_stream[i];
        
        // 根据密钥进行位旋转
        int shift = key_val % 8;
        data[i] = static_cast<uint8_t>((val << shift) | (val >> (8 - shift)));
        
        // 字节置换
        data[i] = static_cast<uint8_t>(data[i] ^ ((key_val * 7 + 13) % 256));
    }
    
    // 第三轮：块间置换（如果数据足够长）
    if (data.size() > 1) {
        for (size_t i = 0; i < data.size() - 1; i += 2) {
            if ((key_stream[i] + key_stream[i + 1]) % 3 == 0) {
                std::swap(data[i], data[i + 1]);
            }
        }
    }
}

void HachimiCore::hachimi_inverse_transform(std::vector<uint8_t>& data, const std::vector<uint8_t>& key_stream) {
    if (data.size() != key_stream.size()) {
        return;
    }
    
    // 逆向第三轮：块间置换
    if (data.size() > 1) {
        for (size_t i = 0; i < data.size() - 1; i += 2) {
            if ((key_stream[i] + key_stream[i + 1]) % 3 == 0) {
                std::swap(data[i], data[i + 1]);
            }
        }
    }
    
    // 逆向第二轮：位移和置换
    for (size_t i = 0; i < data.size(); ++i) {
        uint8_t key_val = key_stream[i];
        
        // 逆向字节置换
        data[i] = static_cast<uint8_t>(data[i] ^ ((key_val * 7 + 13) % 256));
        
        // 逆向位旋转
        uint8_t val = data[i];
        int shift = key_val % 8;
        data[i] = static_cast<uint8_t>((val >> shift) | (val << (8 - shift)));
    }
    
    // 逆向第一轮：XOR操作
    for (size_t i = 0; i < data.size(); ++i) {
        data[i] ^= key_stream[i];
    }
}

} // namespace hachimi