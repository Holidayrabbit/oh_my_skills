---
name: ruby-on-rails-develop
description: Ruby on Rails 全栈开发助手。当用户需要创建、修改或调试 Rails 项目时使用，包括模型设计、控制器编写、路由配置、数据库迁移、视图模板、API 开发、测试编写等。当用户提到 "Rails"、"Ruby on Rails"、"RoR"、"ActiveRecord"、"rake"、"rails generate" 等关键词时触发。
---

# Ruby on Rails 开发助手

协助用户进行 Ruby on Rails 项目的开发、调试与优化。

## 核心原则

1. **遵循 Rails 惯例优于配置（Convention over Configuration）**：优先使用 Rails 约定的命名、目录结构和模式
2. **最小改动原则**：修改代码时只改必要的部分，不做过度重构
3. **代码健壮性**：生成的代码应包含必要的参数校验、错误处理和边界条件处理
4. **简洁注释**：仅在关键逻辑处添加必要的中文注释

## 项目初始化

### 新建项目

```bash
# 标准项目（含前端）
rails new my_app --database=postgresql

# 纯 API 项目
rails new my_api --api --database=postgresql

# 指定 Ruby 版本
rails new my_app --ruby=3.2.0 --database=postgresql
```

### 常用 Gem 推荐

```ruby
# Gemfile 中按需添加
gem 'devise'              # 用户认证
gem 'pundit'              # 权限控制
gem 'kaminari'            # 分页
gem 'ransack'             # 搜索过滤
gem 'sidekiq'             # 后台任务
gem 'redis'               # 缓存/队列
gem 'jbuilder'            # JSON 构建
gem 'rack-cors'           # API 跨域（API 模式）
gem 'annotate'            # 模型字段注释

group :development, :test do
  gem 'rspec-rails'       # 测试框架
  gem 'factory_bot_rails' # 测试数据工厂
  gem 'faker'             # 假数据生成
  gem 'rubocop-rails'     # 代码规范检查
  gem 'pry-rails'         # 调试工具
end
```

## 开发工作流

### 模型（Model）

```bash
# 生成模型
rails generate model User name:string email:string:uniq age:integer admin:boolean

# 生成迁移
rails generate migration AddPhoneToUsers phone:string
rails generate migration CreateJoinTableUsersRoles users roles
```

编写模型时应包含：

```ruby
class User < ApplicationRecord
  # 关联
  has_many :posts, dependent: :destroy
  belongs_to :organization, optional: true

  # 校验
  validates :name, presence: true, length: { maximum: 50 }
  validates :email, presence: true, uniqueness: { case_sensitive: false },
                    format: { with: URI::MailTo::EMAIL_REGEXP }

  # 作用域
  scope :active, -> { where(active: true) }
  scope :recent, -> { order(created_at: :desc) }

  # 回调（谨慎使用）
  before_save :normalize_email

  private

  def normalize_email
    self.email = email.downcase.strip if email.present?
  end
end
```

### 控制器（Controller）

```ruby
class Api::V1::PostsController < ApplicationController
  before_action :authenticate_user!
  before_action :set_post, only: %i[show update destroy]

  def index
    @posts = Post.includes(:user).page(params[:page]).per(20)
    render json: @posts
  end

  def create
    @post = current_user.posts.build(post_params)
    if @post.save
      render json: @post, status: :created
    else
      render json: { errors: @post.errors.full_messages }, status: :unprocessable_entity
    end
  end

  def update
    if @post.update(post_params)
      render json: @post
    else
      render json: { errors: @post.errors.full_messages }, status: :unprocessable_entity
    end
  end

  def destroy
    @post.destroy
    head :no_content
  end

  private

  def set_post
    @post = current_user.posts.find(params[:id])
  end

  def post_params
    params.require(:post).permit(:title, :content, :published)
  end
end
```

### 路由（Routes）

```ruby
Rails.application.routes.draw do
  # API 版本化路由
  namespace :api do
    namespace :v1 do
      resources :posts, only: %i[index show create update destroy] do
        resources :comments, only: %i[index create destroy]
      end
      resources :users, only: %i[show update]
    end
  end

  # 健康检查
  get 'health', to: proc { [200, {}, ['ok']] }
end
```

### 数据库迁移

```ruby
class CreatePosts < ActiveRecord::Migration[7.1]
  def change
    create_table :posts do |t|
      t.string :title, null: false
      t.text :content
      t.boolean :published, default: false, null: false
      t.references :user, null: false, foreign_key: true
      t.timestamps
    end

    add_index :posts, %i[user_id created_at]
    add_index :posts, :published
  end
end
```

```bash
# 迁移命令
rails db:migrate
rails db:rollback STEP=1
rails db:migrate:status
rails db:seed
```

### 服务对象（Service Object）

复杂业务逻辑应抽取到 Service 中：

```ruby
# app/services/posts/create_service.rb
module Posts
  class CreateService
    attr_reader :user, :params

    def initialize(user:, params:)
      @user = user
      @params = params
    end

    def call
      post = user.posts.build(params)

      ActiveRecord::Base.transaction do
        post.save!
        notify_followers(post)
      end

      Result.new(success: true, data: post)
    rescue ActiveRecord::RecordInvalid => e
      Result.new(success: false, errors: e.record.errors.full_messages)
    end

    private

    def notify_followers(post)
      NotifyFollowersJob.perform_later(post.id)
    end
  end
end
```

## 测试编写

### RSpec 基本模式

```ruby
# spec/models/user_spec.rb
RSpec.describe User, type: :model do
  describe 'validations' do
    it { is_expected.to validate_presence_of(:name) }
    it { is_expected.to validate_uniqueness_of(:email).case_insensitive }
  end

  describe 'associations' do
    it { is_expected.to have_many(:posts).dependent(:destroy) }
  end

  describe '#normalize_email' do
    it '保存前将邮箱转为小写' do
      user = create(:user, email: 'TEST@Example.COM')
      expect(user.reload.email).to eq('test@example.com')
    end
  end
end

# spec/requests/api/v1/posts_spec.rb
RSpec.describe 'Api::V1::Posts', type: :request do
  let(:user) { create(:user) }
  let(:headers) { auth_headers(user) }

  describe 'POST /api/v1/posts' do
    let(:valid_params) { { post: { title: 'Test', content: 'Content' } } }

    it '创建成功返回 201' do
      post '/api/v1/posts', params: valid_params, headers: headers
      expect(response).to have_http_status(:created)
      expect(json_response['title']).to eq('Test')
    end
  end
end
```

```bash
# 运行测试
bundle exec rspec
bundle exec rspec spec/models/
bundle exec rspec spec/models/user_spec.rb:15  # 运行指定行
```

## 常用调试命令

```bash
# Rails 控制台
rails console

# 数据库控制台
rails dbconsole

# 查看路由
rails routes
rails routes -g posts  # 过滤包含 posts 的路由

# 查看数据库状态
rails db:migrate:status

# 日志查看
tail -f log/development.log
```

## 性能优化要点

1. **N+1 查询**：使用 `includes`/`preload`/`eager_load` 预加载关联
2. **索引**：为外键和常用查询字段添加数据库索引
3. **缓存**：合理使用 `Rails.cache`、片段缓存和 Russian Doll Caching
4. **后台任务**：耗时操作使用 `ActiveJob` + Sidekiq 异步处理
5. **数据库查询**：用 `select`/`pluck` 只取需要的字段，避免 `SELECT *`
6. **批量操作**：大量数据用 `find_each`/`find_in_batches` 代替 `all.each`

## 安全最佳实践

1. **Strong Parameters**：始终使用 `permit` 白名单过滤参数
2. **CSRF 防护**：API 模式使用 token 认证，非 API 模式保留 CSRF token
3. **SQL 注入**：使用 ActiveRecord 查询接口，避免拼接原始 SQL
4. **密码**：使用 `has_secure_password` 或 Devise，不要自行存储明文密码
5. **敏感配置**：使用 `Rails.application.credentials` 或环境变量管理密钥
